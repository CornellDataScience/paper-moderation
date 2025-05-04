from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import PyPDF2
import io
import os
import logging
from .model import ArxivModel
from pdfminer.high_level import extract_text as pdfminer_extract_text

# Set up logging
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="ArXiv Paper Evaluator API")

# Add CORS middleware to allow frontend to call our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the model
# Update path to point to the models directory inside the API folder
model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")
arxiv_model = ArxivModel(model_path)

@app.post("/evaluate-paper")
async def evaluate_paper(file: UploadFile = File(...)):
    """
    Evaluate if a paper is suitable for arXiv based on the PDF or text file content
    """
    if not (file.filename.endswith('.pdf') or file.filename.endswith('.txt')):
        raise HTTPException(status_code=400, detail="Only PDF and TXT files are accepted")
    
    try:
        # Read the uploaded file
        content = await file.read()
        
        # Extract text based on file type
        if file.filename.endswith('.pdf'):
            # Try using pdfminer.six first (better for scientific papers)
            try:
                text = pdfminer_extract_text(io.BytesIO(content))
                logger.info("Text extracted using pdfminer.six")
            except Exception as e:
                logger.warning(f"pdfminer.six extraction failed: {str(e)}. Falling back to PyPDF2.")
                # Fall back to PyPDF2 if pdfminer fails
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                logger.info("Text extracted using PyPDF2 fallback")
        else:
            # For text files, decode the content directly
            text = content.decode('utf-8')
        
        if not text.strip():
            raise HTTPException(status_code=400, 
                               detail="Could not extract any text from the file. Please ensure the file contains text content.")
        
        logger.info(f"Extracted {len(text)} characters from {'PDF' if file.filename.endswith('.pdf') else 'TXT'}")
        
        # Evaluate the paper using the ML model
        is_approved = arxiv_model.predict(text)
        logger.info(f"Model evaluation result: {is_approved}")
        
        return {"approved": is_approved}
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok"} 