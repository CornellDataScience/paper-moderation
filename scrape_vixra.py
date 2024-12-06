import os
import requests
from bs4 import BeautifulSoup

dir = "vixra_pdfs"
os.makedirs(dir, exist_ok=True)

BASE_URL = "https://vixra.org/all"

def download_pdf(pdf_url, save_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "application/pdf",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }

    response = requests.get(pdf_url, headers=headers, stream=True)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        for content in response.iter_content(chunk_size=8192):
            f.write(content)



def crawler(max_pdfs):
    count = 0
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
}
    response = requests.get(BASE_URL,headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    paragraphs = soup.find_all("p")
    for paragraph in paragraphs:
        if paragraph.find("b"):
            links = paragraph.find_all("a", href=True)
            for link in links:
                if count >= max_pdfs:
                    break
                
                href = link['href']
                if href.endswith(".pdf"):
                    pdf_url = 'https://vixra.org' + href
                    file_name = href.split("/")[-1]
                    save_path = os.path.join(dir, file_name)
                    
                    download_pdf(pdf_url, save_path)
                    print(pdf_url + " downloaded")
                    count += 1
    print('done')

crawler(100)