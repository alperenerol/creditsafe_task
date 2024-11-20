import os
import json
import logging
from config import OUTPUT_DIR, SYSTEM_PROMPT

from src.utils.file_utils import save_json
from src.inference.llama_response import generate_response

def perform_inference(preprocessed_text, pdf_file):
    try:
        # Generate Response
        logging.info(f"Generating LLM response for {pdf_file}")
        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user", 
                "content": preprocessed_text
            }
        ]
        response = generate_response(messages)
        if not response:
            logging.error(f"Empty response received for {pdf_file}. Skipping.")
            return False

        # Convert the response string into a dictionary
        try:
            # Step 1: Clean the response string by removing the backticks and leading/trailing newlines
            cleaned_response = response.strip('`').strip()
            # Step 2: Convert the cleaned response string into a dictionary
            response_dict = json.loads(cleaned_response) 

        except json.JSONDecodeError as e:
            logging.error(f"Error decoding JSON for {pdf_file}: {e}.")
            response_dict = {}

        # Merge 'file_name' into response_dict
        response_dict.update({"file_name": pdf_file})

        # Save Response to JSON
        output_filename = os.path.join(OUTPUT_DIR, 'output.json')

        # Save merged response_dict directly
        save_json(output_filename, response_dict)

    except Exception as e:
        logging.error(f"Error generating response from LLM: {str(e)}")