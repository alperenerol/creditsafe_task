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
                {"role": "system", "content": "From the following text: Extract the following informations and provide as JSON format output, Information to be extracted: Company Name, Company Identifier, Document Purpose, Relevant fields about Document Purpose from Document Purpose content. Include all relevant information about Document Purpose and include as keys in json format output under Document Purpose key. Just return the JSON dict."},
                {"role": "user", "content": """N° d'entreprise : 0567 779 701
            en enter): ADAM PARTENARIAT |
            {en abreqgé)
            Forme légale : SOCIETE A RESPONSABILITE LIMITEE
            Adresse compléte du siege : AVENUE DES PAGODES 198 - 1020 BRUXELLES
            Objet de Vacte : DEMISSION - NOMINATION - CESSION DE PARTS SOCIALES
            Extrait de l'assembiée générale extraordinaire du 14 décembre 2023"""}]
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
    #extract_and_preprocess()
    perform_inference()
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