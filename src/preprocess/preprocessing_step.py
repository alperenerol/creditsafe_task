import os
import logging

from src.utils.file_utils import save_text, get_preprocessed_text_path
from src.preprocess.text_operations import process_text


def raw_text_preprocess(raw_text_content, pdf_file, text_dir):
    # Check if preprocessed text already exists
    preprocessed_text_path = get_preprocessed_text_path(pdf_file, text_dir)

    if os.path.exists(preprocessed_text_path):
        logging.info(
            f"Preprocessed text already exists for {pdf_file}. Skipping preprocessing."
        )

        try:
            with open(preprocessed_text_path, "r", encoding="utf-8") as file:
                preprocessed_text = file.read()
            return preprocessed_text  # Return the loaded preprocessed text

        except Exception as e:
            logging.error(
                f"Error reading preprocessed text from {preprocessed_text_path} for {pdf_file}: {str(e)}"
            )
            return None

    try:
        preprocessed_text_path = get_preprocessed_text_path(pdf_file, text_dir)
        # Preprocess Text
        preprocessed_text = process_text(raw_text_content)

        if not preprocessed_text:
            logging.error(
                f"Error processing extracted text of {pdf_file}. No text was generated during preprocessing."
            )  # Log if preprocessing fails
            return None

        # Save Preprocessed Text
        save_text(preprocessed_text_path, preprocessed_text)
        logging.info(f"Preprocessed text saved for {pdf_file}")

        return preprocessed_text

    except Exception as e:
        logging.error(f"Error processing extracted text of {pdf_file}: {str(e)}")
        return None
