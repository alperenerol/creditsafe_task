import os
import json
import logging

from config import TEXT_DIR
from src.utils.error_utils import handle_errors

@handle_errors(log_message="Error during saving text")
def save_text(output_filename, text):
    # Save the preprocessed text to a file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)

@handle_errors(log_message="Error during saving JSON")
def save_json(output_filename, new_data):
    """
    Appends a new dictionary to an existing JSON file or creates the file if it doesn't exist.

    Args:
        file_path (str): The path to the JSON file.
        new_data (dict): The new dictionary to append to the JSON file.
    """
    # Check if the file exists
    if os.path.exists(output_filename):
        # Load the existing data
        with open(output_filename, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)  # Load existing data into a list
                if not isinstance(data, list):
                    raise ValueError(f"Expected a list in {output_filename}, but got {type(data).__name__}")
            except json.JSONDecodeError:
                # If the file is empty or contains invalid JSON, start with an empty list
                data = []
    else:
        # If file does not exist, start with an empty list
        data = []

    # Append the new data to the list
    data.append(new_data)

    # Save the updated list back to the JSON file
    with open(output_filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    logging.info(f"New LLM response data appended to output file.")

def get_raw_text_path(pdf_file, text_dir=TEXT_DIR):
    return os.path.join(text_dir, pdf_file.replace('.pdf', '_raw.txt'))

def get_preprocessed_text_path(pdf_file, text_dir=TEXT_DIR):
    return os.path.join(text_dir, pdf_file.replace('.pdf', '_preprocessed.txt'))
