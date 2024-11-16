import logging
from src.utils.error_utils import handle_errors

@handle_errors(log_message="Error during saving text")
def save_text(output_filename, text):
    # Save the preprocessed text to a file
    with open(output_filename, 'w', encoding='utf-8') as f:
        f.write(text)

@handle_errors(log_message="Error during saving JSON")
def save_json(output_filename, data):
    # Save the JSON data to a file
    import json
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)