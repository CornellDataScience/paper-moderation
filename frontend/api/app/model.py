import os
import re
from transformers import AutoTokenizer, LongformerForSequenceClassification
import torch

class ArxivModel:
    def __init__(self, model_dir):
        """
        Initialize the arXiv paper evaluator model
        
        Args:
            model_dir: Directory containing the model files
        """
        self.model_dir = model_dir
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_model()
        
    def load_model(self):
        """Load the model and tokenizer from files"""
        try:
            # Load the model configuration - use Longformer for sequence classification
            self.tokenizer = AutoTokenizer.from_pretrained("allenai/longformer-base-4096")
            self.model = LongformerForSequenceClassification.from_pretrained(self.model_dir)
            self.model.to(self.device)
            self.model.eval()  # Set model to evaluation mode
            print(f"Model loaded successfully to {self.device}")
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_text(self, text):
        """
        Preprocess text the same way as during training:
        1. Keep only ASCII characters
        2. Remove specific words
        3. Normalize whitespace
        """
        # Keep only ASCII characters (0-127)
        processed_text = ''.join([char for char in text if ord(char) < 128])
        
        # Define words to delete
        delete_words = ['http', 'www', 'vixra', 'arxiv', 'cid', 'dis', 'ik', 'q2', 'q1', 'th', 'rst', 'ed', 'nd', 'yahoo', 'com']
        
        # Split into words, filter, and rejoin
        words = processed_text.split()
        filtered_words = []
        
        for word in words:
            # Check if any of the delete_words exist, and don't add if they do
            if not any(term.lower() in word.lower() for term in delete_words):
                filtered_words.append(word)
        
        # Rejoin the filtered words back into text
        filtered_text = ' '.join(filtered_words)
        
        # Normalize whitespace
        filtered_text = re.sub(r'\s+', ' ', filtered_text).strip()
        
        return filtered_text
    
    def predict(self, text):
        """
        Predict whether a paper is suitable for arXiv
        
        Args:
            text: The extracted text from the PDF
            
        Returns:
            bool: True if the paper is approved, False otherwise
        """
        try:
            # Apply the same preprocessing as during training
            preprocessed_text = self.preprocess_text(text)
            
            # Tokenize the input text with the same parameters as in training
            inputs = self.tokenizer(
                preprocessed_text,
                return_tensors="pt",
                truncation=True,
                max_length=4096,  # Use same max_length as in training
                padding="max_length"
            ).to(self.device)
            
            # Forward pass through model
            with torch.no_grad():
                outputs = self.model(**inputs)
                
            # Get prediction (assuming binary classification where 1 is "approved")
            logits = outputs.logits
            probabilities = torch.softmax(logits, dim=1)
            prediction = torch.argmax(probabilities, dim=1).item()
            
            return prediction == 1  # True if prediction is 1, False otherwise
            
        except Exception as e:
            print(f"Error during prediction: {str(e)}")
            # Default to False in case of errors
            return False 