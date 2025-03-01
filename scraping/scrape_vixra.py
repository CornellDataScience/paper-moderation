import os
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader
import boto3

obj = boto3.client("s3")

count = 0
real_count = 0
BASE_URL = "https://vixra.org/all"

def send_to_s3(filename):
    global real_count
    s3_key = "vixra_papers/"+filename
    try:
        # Check if the file already exists in S3
        obj.head_object(Bucket="arxivpapers", Key=s3_key)
        print(f"{filename} already exists in S3, skipping upload.")
        return False
    except obj.exceptions.ClientError as e:
        # If the error is not a 404, raise it
        if e.response['Error']['Code'] != "404":
            raise
        print(f"{filename} not found in S3, uploading.")
    
    try:
        # Upload the file if it doesn't exist
        obj.upload_file(
            Filename=filename,
            Bucket="arxivpapers",
            Key=s3_key
        )
        real_count += 1
        print(f"Uploaded {filename} to S3, real count = {real_count}")
        return True
    except Exception as e:
        print(f"Failed to upload {filename} to S3. Error: {e}")
        raise e


def download_pdf(pdf_url, save_path):
    global count
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/pdf",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    if os.path.exists(save_path):
        print('Already downloaded ' + save_path)
        return True

    try:
        if count <= 33532:
            count += 1
            print('Already downloaded ' + save_path +" count is "+ str(count))
            return False
        response = requests.get(pdf_url, headers=headers, stream=True)
        with open(save_path, "wb") as f:
            for content in response.iter_content(chunk_size=8192):
                f.write(content)
        count += 1
        print(f"Downloaded: {pdf_url}, total = {count}")
        return True
    except Exception as e:
        print(f"Failed to download {pdf_url}. Error: {e}")
        return False

def convert_pdf_to_text(pdf_path, text_path):
    try:
        if os.path.exists(text_path):
            print('Already converted ' + text_path)
            return 
        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
        
        with open(text_path, "w", encoding="utf-8") as text_file:
            text_file.write(text)
        print(f"Converted {pdf_path} to {text_path}")
    except Exception as e:
        print(f"Failed to convert {pdf_path} to text. Error: {e}")

def crawler(url, visited=None):
    global count
    if visited is None:
        visited = set()

    if url in visited:
        print('Already visited ' + url)
        return
    visited.add(url)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        links = soup.find_all("a", href=True)
        for link in links:
            href = link['href']
            if href.endswith(".pdf"):
                pdf_url = href if href.startswith("http") else 'https://vixra.org' + href
                file_name = href.split("/")[-1]
                save_path = file_name
                text_path = save_path.replace(".pdf", ".txt")
                visited.add(pdf_url)
                
                if download_pdf(pdf_url, save_path):
                    convert_pdf_to_text(save_path, text_path)
                    try:
                        send_to_s3(text_path)
                    finally:
                        os.remove(save_path)
                        os.remove(text_path)
            elif href.startswith("/") and 'all' not in href:
                next_page_url = 'https://vixra.org' + href
                crawler(next_page_url, visited)
    except Exception as e:
        print(f"Failed to process {url}. Error: {e}")

# Start crawling
crawler(BASE_URL)
