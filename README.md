# Project Name: PDF Information Extraction and Inference

## Overview

This project is a complete pipeline for extracting and processing information from PDF documents using Tesseract OCR (Optical Character Recognition) library and an LLM (Large Language Model) to derive structured information. It supports concurrent processing for speed, error handling, and adheres to specific formatting requirements. The main components are:

Text Extraction: Extract text from PDFs using Tesseract OCR library. It first convert PDF into lossless image format(.png), then extracts text from the images. 

Text Preprocessing: Process extracted raw text to clean and prepare for inference.

Inference: Utilize the Llama 3.1-70B-Versatile model to infer and structure the extracted information into a JSON format.

## Features

Concurrent PDF Processing: Uses ProcessPoolExecutor to process multiple PDFs concurrently.

Error Handling: Comprehensive error handling for failed OCR, preprocessing, and LLM inference steps.

Configurable: All paths and settings, including API keys, PDF directories, and log file paths, are customizable.

Structured Output: Extracted information is saved as structured JSON files for easy integration.

Tests: Unit tests are provided for each step to ensure reliability.

## Project Structure
```sh
project-root/
├── config.py
├── main.py
├── src/
│   ├── extract/
│   │   ├── ocr_operations.py
│   │   └── pdf_extraction_step.py
│   ├── preprocess/
│   │   ├── text_operations.py
│   │   └── preprocessing_step.py
│   ├── inference/
│   │   ├── inference_step.py
│   │   └── llama_response.py
│   └── utils/
│       ├── file_utils.py
│       ├── error_utils.py
│       └── logging_utils.py
├── tests/
│   ├── test_file_utils.py
│   ├── test_inference_step.py
│   └── test_pdf_extraction_step.py
│   └── test_preprocessing_step.py
├── data/
│   ├── pdfs/
│   ├── text/
│   ├── outputs/
├── logs/
├── Dockerfile
├── README.md
└── requirements.txt
```
## Requirements

Stable internet connection

Python 3.10+

Tesseract OCR (for OCR extraction)

Poppler

Install all the dependencies using pip:

```pip install -r requirements.txt```

## Setup Instructions

### 1. Install Tesseract OCR and Poppler

Make sure to install Poppler before running the project. On Ubuntu, you can do so with:

```sh
   sudo apt-get update
   sudo apt-get install -y poppler-utils
   sudo apt-get install -y tesseract-ocr
```

### 2. Configure Project

Modify the config.py file to specify your directory paths and API keys:

PDF_DIR: Path to the directory containing PDF files.

TEXT_DIR: Path to save extracted and preprocessed text files.

OUTPUT_DIR: Path to save output JSON files.

LOG_FILE: Path for log files.

GROQ_API_KEY: API key for LLM inference.

SYSTEM_PROMPT: The system prompt for LLM inference to structure output correctly.

### 3. Run the Project

You can run the entire workflow with:

```python main.py```

This will:

Extract text from PDF files.

Preprocess the extracted text.

Perform inference using the Llama 3.1-70B-Versatile model.

Save the results as JSON file.

### 4. Running Tests

Unit tests are available to ensure everything works as expected. To run the tests, use:

```python -m unittest discover tests```

## Detailed Workflow

### 1. Text Extraction

The pdf_extract() function in ocr_extraction.py extracts text from PDF files using OCR and saves the extracted raw text to the disk.

The extraction step checks if a file has already been processed to prevent redundant work.

### 2. Text Preprocessing

The raw_text_preprocess() function in text_operations.py processes raw text files to clean and normalize them.

The preprocessed text is then saved in a separate directory.

### 3. LLM Inference

The perform_inference() function in inference.py sends the preprocessed text to the Llama 3.1-70B-Versatile model via the GroqCloud API to generate a structured JSON response.

The LLM system prompt specifies how to extract specific details, such as the Company Name, Company Identifier, and Document Purpose.

The output is saved as a JSON file, with error handling for invalid responses and rate limit retries.

### 4. Rate Limiting and Retries

The API handles rate limits automatically to avoid overwhelming the LLM API.

### Example Output

For an input PDF "24000009.pdf" containing company information, the output is structured as follows:

```json
{
    "Company Name": "JANSE",
    "Company Identifier": "415121990",
    "Document Purpose": {
        "Event": "Renewal of Board of Directors",
        "Decision": "Appointment of Directors",
        "Date of Decision": "October 2, 2023",
        "Duration of Mandate": "3 years",
        "Compensation": "Free of charge",
        "New Administrators": [
            "Mr. Jean Simons",
            "Ms. Brigitte Schrurs",
            "Ms. Madeleine Simons"
        ]
    },
}
```

### Running with Docker (Optional)

If you'd like to run the project inside a Docker container, follow these instructions:

### Prerequisites

Docker: Make sure Docker is installed on your system. You can download Docker from https://www.docker.com/products/docker-desktop.

### Build the Docker Image Locally

You can build a Docker image of this project to avoid manual dependency installation:

```docker build -t task_ocr_llm .```

### Running the Container

To run the Docker container:

```docker run -it --rm -v $(pwd)/data:/workspace/data task_ocr_llm python main.py```

This command mounts the output folder in your current directory so you can easily access the results.

### Running Tests in Docker

You can also run the tests within the Docker container:

```docker run -it --rm -v $(pwd)/data:/workspace/data task_ocr_llm python -m unittest discover tests```

