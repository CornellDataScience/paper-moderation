# ArXiv Paper Evaluator API

This API provides an endpoint to evaluate whether a paper is suitable for arXiv based on its content using a machine learning model.

## Setup

1. Ensure you have Python 3.8+ installed

2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

3. Make sure your model files are in the correct location. The API expects to find the following files in the API root directory:
   - training_args.bin
   - trainer_state.json
   - scheduler.pt
   - rng_state.pth
   - optimizer.pt
   - model.safetensors
   - config.json

## Testing the Model

Before running the API server, you can verify that the model loads correctly by running:

```
python test_model.py
```

This script will:

1. Try to load the model
2. Run a sample prediction
3. Display the result

## Running the API

Start the API server with:

```
cd api
python run.py
```

The API will be available at http://localhost:8000

## API Endpoints

- `POST /evaluate-paper`: Evaluates if a paper is suitable for arXiv

  - Accepts a PDF file upload
  - Returns `{"approved": true}` or `{"approved": false}`

- `GET /health`: Health check endpoint
  - Returns `{"status": "ok"}` if the API is running

## Integration with Frontend

The frontend React application is configured to communicate with this API at http://localhost:8000. Make sure both the frontend and backend are running simultaneously for the complete application to work.

## Technical Details

### Text Preprocessing

The API applies the following preprocessing steps to PDF content:

1. Extract text from all PDF pages
2. Remove non-ASCII characters (keeping only characters with ASCII values 0-127)
3. Remove specific words like 'http', 'www', 'vixra', 'arxiv', etc.
4. Normalize whitespace

### Model

The system uses a Longformer model for sequence classification with:

- Maximum sequence length of 4096 tokens
- Binary classification (suitable vs. not suitable for arXiv)

This matches the preprocessing and model configuration used during training.
