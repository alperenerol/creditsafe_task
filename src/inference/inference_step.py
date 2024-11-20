import os
import json
import logging
from config import OUTPUT_DIR

from src.utils.file_utils import save_json
from src.inference.llama_response import generate_response

def perform_inference(preprocessed_text, pdf_file):
    try:
        # Generate Response
        logging.info(f"Generating LLM response for {pdf_file}")
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
            logging.error(f"Error decoding JSON for {pdf_file}: {e}. Response was: {response}")
            response_dict = {}

        # Merge 'file_name' into response_dict
        response_dict.update({"file_name": pdf_file})

        # Save Response to JSON
        output_filename = os.path.join(OUTPUT_DIR, 'output.json')

        # Save merged response_dict directly
        save_json(output_filename, response_dict)
        logging.info(f"Inference complete for {pdf_file}")

    except Exception as e:
        logging.error(f"Error generating response from LLM: {str(e)}")