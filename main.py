import os
import logging
#import argparse
import json
from config import PDF_DIR, TEXT_DIR, OUTPUT_DIR, LOG_FILE
from src.extract.ocr_extraction import extract_text
from src.preprocess.text_preprocessing import preprocess_text
from src.inference.llama_inference import generate_response
from src.utils.file_utils import save_text, save_json
from src.utils.logging_utils import setup_logging, reset_logging

# Set up logging
setup_logging(log_file=LOG_FILE, level=logging.INFO, console=True)

def pdf_extract():
    # Step 1: Extract Text and Preprocess
    logging.info("Starting extraction and preprocessing...")

    # Get list of all PDF files
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)

        try:
            # Extract Text
            logging.info(f"Extracting text from {pdf_file}")
            raw_text = extract_text(pdf_path)
            if not raw_text:
                continue  # Skip to the next file if extraction fails

            # Save Extracted Raw Text
            raw_text_path = os.path.join(TEXT_DIR, pdf_file.replace('.pdf', '_raw.txt'))
            save_text(raw_text_path, raw_text)
            logging.info(f"Raw text saved for {pdf_file}")

        except Exception as e:
            logging.error(f"Error processing {pdf_file}: {str(e)}")

def raw_text_preprocess():
    # Step 1: Preprocess extracted raw text
    logging.info("Starting text preprocessing...")

    # Get list of all raw text files
    raw_text_files = [f for f in os.listdir(TEXT_DIR) if f.endswith('_raw.txt')]

    for raw_text_file in raw_text_files:
        raw_text_path = os.path.join(TEXT_DIR, raw_text_file)
        pdf_file = raw_text_file.replace('_raw.txt', '.pdf')
        try:
            # **Read the raw text from the file**
            with open(raw_text_path, 'r', encoding='utf-8') as f:
                raw_text_content = f.read()
            
            # Preprocess Text
            logging.info(f"Preprocessing extracted text from {pdf_file}")
            preprocessed_text = preprocess_text(raw_text_content)
            if not preprocessed_text:
                continue  # Skip to the next file if preprocessing fails

            # Save Preprocessed Text
            preprocessed_text_path = os.path.join(TEXT_DIR, pdf_file.replace('.pdf', '_preprocessed.txt'))
            save_text(preprocessed_text_path, preprocessed_text)
            logging.info(f"Preprocessed text saved for {pdf_file}")

        except Exception as e:
            logging.error(f"Error processing {raw_text_file}: {str(e)}")

def perform_inference():
    # Step 2: Inference
    logging.info("Starting inference...")

    # Get list of all preprocessed text files
    preprocessed_text_files = [f for f in os.listdir(TEXT_DIR) if f.endswith('preprocessed.txt')]

    for text_file in preprocessed_text_files:
        text_path = os.path.join(TEXT_DIR, text_file)
        try:
            # Load Preprocessed Text
            with open(text_path, 'r', encoding='utf-8') as f:
                preprocessed_text = f.read()

            # Generate Response
            logging.info(f"Generating response for {text_file}")
            messages = [
                {
                    "role": "system",
                    "content": (
                        "You are an information extraction assistant. Your task is to extract specific information from the provided text "
                        "and return it in a structured JSON format. Follow these instructions closely for the best results.\n\n"
                        "From the following text, extract the specified information and return it as a JSON object.\n\n"
                        "Information to extract:\n"
                        "    1. Company Name: The full legal name of the company.\n"
                        "    2. Company Identifier: Any unique identifier for the company (e.g., registration number).\n"
                        "    3. Document Purpose: Include all relevant and important fields about the document purpose from the text under the 'Document Purpose' section.\n"
                        "        - Each piece of information should be included as a separate key within the 'Document Purpose' key.\n\n"
                        "Output Requirements:\n"
                        "    - Return only the JSON object with no additional text or explanations.\n"
                        "    - Ensure the JSON object is well-formatted and complete."
                    )
                },
                {
                    "role": "user", 
                    "content": preprocessed_text
                }
            ]
            response = generate_response(messages)
            # Convert the response string into a dictionary
            try:
                # Step 1: Clean the response string by removing the backticks and leading/trailing newlines
                cleaned_response = response.strip('`').strip()
                # Step 2: Convert the cleaned response string into a dictionary
                response_dict = json.loads(cleaned_response)    
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
                response_dict = {}

            # Save Response to JSON
            output_filename = os.path.join(OUTPUT_DIR, text_file.replace('_preprocessed.txt', '.json'))
            # Merge 'file_name' into response_dict
            response_dict.update({"file_name": text_file.replace('_preprocessed.txt', '.pdf')})
            # Save merged response_dict directly
            save_json(output_filename, response_dict)

            logging.info(f"Inference complete for {text_file}")

        except Exception as e:
            logging.error(f"Error processing {text_file}: {str(e)}")

if __name__ == "__main__":
    pdf_extract()
    raw_text_preprocess()
    perform_inference()
    reset_logging()