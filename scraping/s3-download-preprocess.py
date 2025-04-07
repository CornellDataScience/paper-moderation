import os
import re
import random
import boto3
from datasets import Dataset
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# 1. Download files from S3 bucket
def download_files_from_s3(bucket_name, prefix, local_dir):
    """
    Download all files from an S3 bucket prefix to a local directory
    """
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
    
    # Get AWS credentials from environment variables
    aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-2")
    
    # Create S3 client with credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    
    # List objects in the prefix
    print(f"Listing objects in s3://{bucket_name}/{prefix}/")
    paginator = s3.get_paginator('list_objects_v2')
    objects = []
    
    for page in paginator.paginate(Bucket=bucket_name, Prefix=prefix):
        if 'Contents' in page:
            for obj in page['Contents']:
                if obj['Key'].endswith('.txt'):
                    objects.append(obj['Key'])
    
    print(f"Found {len(objects)} files in {prefix}/")
    
    # Download each file
    for i, key in enumerate(tqdm(objects, desc=f"Downloading {prefix} files")):
        local_file = os.path.join(local_dir, os.path.basename(key))
        s3.download_file(bucket_name, key, local_file)
    
    return len(objects)

def preprocess_text_file(file_path):
    """
    Preprocess a text file to:
    1. Remove extra spaces, multiple newlines, and special characters.
    2. Contain only ASCII characters (0-127)
    3. Remove web-related terms (http, www) and unwanted phrases (vixra, arxiv)
    """
    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
        text = f.read()

    # Keep only ASCII characters (characters with ASCII values 0-127)
    processed_text = ''
    for char in text:        
        if ord(char) < 128:  # ASCII characters have values 0-127
            processed_text += char
                
    delete_words = ['http', 'www', 'vixra', 'arxiv']
    
    # Split into words, filter, and rejoin
    words = processed_text.split()
    filtered_words = []
    
    for word in words:
        # check if any of the delete_words exist, and don't add if they do
        if not any(term.lower() in word.lower() for term in delete_words):
            filtered_words.append(word)
    
    # Rejoin the filtered words back into text
    filtered_text = ' '.join(filtered_words)
    
    return filtered_text
    
    # Normalize whitespace
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()
    
    return processed_text

# 3. Split data and 4. Create datasets
def create_datasets(arxiv_dir, vixra_dir, output_dir, sample_dir):
    """
    Create and save train/val/test datasets from the preprocessed files
    
    Args:
        arxiv_dir: Directory containing preprocessed arxiv text files
        vixra_dir: Directory containing preprocessed vixra text files
        output_dir: Directory to save the datasets
        sample_dir: Directory to save sample files
    """
    # Get all preprocessed files
    arxiv_files = [os.path.join(arxiv_dir, f) for f in os.listdir(arxiv_dir) if f.endswith('.txt')]
    vixra_files = [os.path.join(vixra_dir, f) for f in os.listdir(vixra_dir) if f.endswith('.txt')]
    
    print(f"Found {len(arxiv_files)} arxiv files and {len(vixra_files)} vixra files")
    
    # Shuffle files to ensure randomness
    random.shuffle(arxiv_files)
    random.shuffle(vixra_files)
    
    # Create sample directory for inspection
    if not os.path.exists(sample_dir):
        os.makedirs(sample_dir)
    
    # Save 10 examples of each for inspection
    for i, file_path in enumerate(arxiv_files[:10]):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            text_content = f.read()
        sample_path = os.path.join(sample_dir, f"arxiv_sample_{i}.txt")
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
    
    for i, file_path in enumerate(vixra_files[:10]):
        with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
            text_content = f.read()
        sample_path = os.path.join(sample_dir, f"vixra_sample_{i}.txt")
        with open(sample_path, 'w', encoding='utf-8') as f:
            f.write(text_content)
    
    # Calculate split sizes
    min_class_size = min(len(arxiv_files), len(vixra_files))
    train_size = int(min_class_size * 0.7)
    val_size = int(min_class_size * 0.15)
    test_size = min_class_size - train_size - val_size
    
    # Create equal-sized splits for both classes
    arxiv_train = arxiv_files[:train_size]
    arxiv_val = arxiv_files[train_size:train_size+val_size]
    arxiv_test = arxiv_files[train_size+val_size:train_size+val_size+test_size]
    
    vixra_train = vixra_files[:train_size]
    vixra_val = vixra_files[train_size:train_size+val_size]
    vixra_test = vixra_files[train_size+val_size:train_size+val_size+test_size]
    
    # Create and save datasets
    splits = {
        'train': (arxiv_train, vixra_train),
        'validation': (arxiv_val, vixra_val),
        'test': (arxiv_test, vixra_test)
    }
    
    for split_name, (arxiv_split, vixra_split) in splits.items():
        texts = []
        labels = []
        
        # Add arxiv papers (label 1)
        for file_path in tqdm(arxiv_split, desc=f"Processing arxiv {split_name}"):
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                text_content = f.read()
            texts.append(text_content)
            labels.append(1)
        
        # Add vixra papers (label 0)
        for file_path in tqdm(vixra_split, desc=f"Processing vixra {split_name}"):
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                text_content = f.read()
            texts.append(text_content)
            labels.append(0)
        
        # Create dataset
        df = pd.DataFrame({
            'text': texts,
            'labels': labels
        })
        
        # Shuffle the dataset
        df = df.sample(frac=1, random_state=42).reset_index(drop=True)
        
        # Convert to HuggingFace Dataset
        dataset = Dataset.from_pandas(df)
        
        # Save as arrow file
        output_path = os.path.join(output_dir, split_name)
        if not os.path.exists(output_path):
            os.makedirs(output_path)
        
        dataset.save_to_disk(output_path)
        print(f"Saved {split_name} dataset with {len(dataset)} examples")

def main():
    # Load environment variables from .env file
    load_dotenv()
    
    # Configuration
    bucket_name = os.getenv("AWS_S3_BUCKET_NAME")
    base_dir = "s3-scraping"
    
    # Local directories
    raw_arxiv_dir = os.path.join(base_dir, "raw_arxiv")
    raw_vixra_dir = os.path.join(base_dir, "raw_vixra")
    
    processed_arxiv_dir = os.path.join(base_dir, "processed_arxiv")
    processed_vixra_dir = os.path.join(base_dir, "processed_vixra")
    
    sample_dir = os.path.join(base_dir, "samples")
    output_dir = os.path.join(base_dir, "datasets")
    
    # Create directories
    for directory in [base_dir, raw_arxiv_dir, raw_vixra_dir, processed_arxiv_dir, processed_vixra_dir, output_dir]:
        if not os.path.exists(directory):
            os.makedirs(directory)
    
    # 1. Download files from S3
    # print("Step 1: Downloading files from S3")
    # arxiv_count = download_files_from_s3(bucket_name, "arxiv_papers", raw_arxiv_dir)
    # vixra_count = download_files_from_s3(bucket_name, "vixra_papers", raw_vixra_dir)
    
    # 2. Preprocess files
    print("\nStep 2: Preprocessing files")
    # Process arxiv files
    for filename in tqdm(os.listdir(raw_arxiv_dir), desc="Processing arxiv files"):
        if filename.endswith('.txt'):
            input_path = os.path.join(raw_arxiv_dir, filename)
            output_path = os.path.join(processed_arxiv_dir, filename)
            
            processed_text = preprocess_text_file(input_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
    
    # Process vixra files
    for filename in tqdm(os.listdir(raw_vixra_dir), desc="Processing vixra files"):
        if filename.endswith('.txt'):
            input_path = os.path.join(raw_vixra_dir, filename)
            output_path = os.path.join(processed_vixra_dir, filename)
            
            processed_text = preprocess_text_file(input_path)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(processed_text)
    
    # 3 & 4. Create datasets
    print("\nStep 3 & 4: Creating and saving datasets")
    create_datasets(processed_arxiv_dir, processed_vixra_dir, output_dir, sample_dir)
    
    print("\nAll tasks completed successfully!")
    print(f"Samples saved to: {sample_dir}")
    print(f"Datasets saved to: {output_dir}")

if __name__ == "__main__":
    main()