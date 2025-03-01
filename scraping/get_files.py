import json
import os
import re
import boto3

obj = boto3.client("s3")
count = 0
def send_to_s3(filename):
    obj.upload_file(
    Filename= filename,
    Bucket="arxivpapers",
    Key="arxiv_papers/"+filename
)

entries = []

with open('test.json', 'r', encoding='utf-8') as file:
    with open('test.json', 'r', encoding='utf-8') as file:
        for i, line in enumerate(file):
            if i < 31000:
                entries.append(json.loads(line))
            else: 
                break

for entry in entries:
    paper_id = entry.get("paper_id")
    paper_id = re.sub(r'\.', '_', paper_id)
    paper_id = paper_id.replace("/", "_").replace("\\", "_")
    text = entry.get("fulltext")
    
    if paper_id and text:
        with open(paper_id + '.txt', 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
        send_to_s3(paper_id + '.txt')
        count += 1
        print(count)
        os.remove(paper_id + '.txt')
