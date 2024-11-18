import json
import os
import re

os.makedirs('arxiv_papers')

entries = []

with open('test.json', 'r', encoding='utf-8') as file:
    for i, line in enumerate(file):
        if i >= 100:
            break
        entries.append(json.loads(line))

for entry in entries:
    paper_id = entry.get("paper_id")
    paper_id = re.sub(r'\.', '_', paper_id)
    paper_id = paper_id.replace("/", "_").replace("\\", "_")
    text = entry.get("fulltext")
    print(text)
    
    # Check if required fields are present
    if paper_id and text:
        txt_file_path = os.path.join('arxiv_papers', f"{paper_id}.txt")
        with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)
