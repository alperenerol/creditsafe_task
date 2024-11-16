import os
import logging
#import argparse
from config import PDF_DIR, TEXT_DIR, OUTPUT_DIR, LOG_FILE
from src.extract.ocr_extraction import extract_text
from src.preprocess.text_preprocessing import preprocess_text
#from src.inference.llama_inference import generate_response_from_llama
from src.utils.file_utils import save_text # save_json
from src.utils.logging_utils import setup_logging, reset_logging

# Set up logging
setup_logging(log_file=LOG_FILE, level=logging.INFO, console=True)

def extract_and_preprocess():
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
            raw_text_filename = os.path.join(TEXT_DIR, pdf_file.replace('.pdf', '_raw.txt'))
            save_text(raw_text_filename, raw_text)
            logging.info(f"Raw text saved for {pdf_file}")

            # Preprocess Text
            logging.info(f"Preprocessing extracted text from {pdf_file}")
            preprocessed_text = preprocess_text(raw_text)
            if not preprocessed_text:
                continue  # Skip to the next file if preprocessing fails

            # Save Preprocessed Text
            preprocessed_text_filename = os.path.join(TEXT_DIR, pdf_file.replace('.pdf', '_preprocessed.txt'))
            save_text(preprocessed_text_filename, preprocessed_text)
            logging.info(f"Preprocessed text saved for {pdf_file}")

        except Exception as e:
            logging.error(f"Error processing {pdf_file}: {str(e)}")

if __name__ == "__main__":
    extract_and_preprocess()
    reset_logging()


























""" def main():
    # Setup logging
    setup_logging(log_file='logs/process.log')

    # Get list of all PDF files
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith('.pdf')]

    for pdf_file in pdf_files:
        pdf_path = os.path.join(PDF_DIR, pdf_file)

        try:
            # Step 1: Extract Text
            logging.info(f"Extracting text from {pdf_file}")
            text = extract_text_from_pdf_ocr(pdf_path)
            
            # Step 2: Preprocess Text
            logging.info(f"Preprocessing the extracted text from {pdf_file}")
            preprocessed_text = preprocess_text(text)

            # Step 3: Inference
            logging.info(f"Generating response for {pdf_file}")
            prompt = "Summarize the key points of the following text:"
            response = generate_response_from_llama(preprocessed_text, prompt)

            # Step 4: Save Response to JSON
            output_filename = os.path.join(OUTPUT_DIR, pdf_file.replace('.pdf', '.json'))
            save_json(output_filename, {"file_name": pdf_file, "response": response})

            logging.info(f"Processing complete for {pdf_file}")

        except Exception as e:
            logging.error(f"Error processing {pdf_file}: {str(e)}")

if __name__ == "__main__":
    main()
    extract_and_preprocess() """