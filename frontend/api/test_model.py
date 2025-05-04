#!/usr/bin/env python3
"""
Test script to verify model loading and inference.
Run this script after setting up the model files to ensure everything works.
"""
import os
import sys
from app.model import ArxivModel

def test_model():
    """Test the ArXiv model loading and a simple prediction"""
    print("Testing ArXiv model loading and prediction...")
    
    # Get the current directory (should be the api directory)
    model_dir = os.path.dirname(os.path.abspath(__file__))
    
    try:
        # Attempt to load the model
        print(f"Loading model from {model_dir}...")
        model = ArxivModel(model_dir)
        print("Model loaded successfully!")
        
        # Try a simple prediction with a test string
        test_text = """
        This paper presents a new approach to quantum field theory that unifies gravitational 
        and electromagnetic forces. We demonstrate through mathematical proofs and simulation
        that our approach resolves long-standing issues in theoretical physics.
        Our findings suggest a novel interpretation of quantum mechanics that is consistent with
        general relativity and provides testable predictions for future experiments.
        """
        
        print("\nTesting prediction with sample text...")
        result = model.predict(test_text)
        
        print(f"\nPrediction result: {'APPROVED' if result else 'REJECTED'}")
        print("Test completed successfully!")
        return 0
        
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(test_model()) 