
from PyPDF2 import PdfReader
import os

os.makedirs('vixra_txt', exist_ok=True)

    
for file in os.listdir('vixra_pdfs'):
      pdf_path = os.path.join('vixra_pdfs', file)
      txt_file = os.path.splitext(file)[0] + '.txt'
      txt_path = os.path.join('vixra_txt', txt_file)
      with open(pdf_path, 'rb') as pdf_file:
        reader = PdfReader(pdf_file)
        text = ""
        
        for page in reader.pages:
            text += page.extract_text()

        with open(txt_path, 'w', encoding='utf-8') as txt_file:
            txt_file.write(text)