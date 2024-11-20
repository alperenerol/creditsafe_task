import os
import logging
from config import PDF_DIR, TEXT_DIR

from src.utils.file_utils import save_text, get_raw_text_path
from src.extract.ocr_operations import extract_text_ocr


def pdf_extract(pdf_file, pdf_dir=PDF_DIR):
    """
    Extract text from a PDF and save it to disk, if the raw text file does not already exist.

    Args:
        pdf_file (str): The filename of the PDF file.

    Returns:
        tuple: (raw_text, pdf_file) if extraction was successful, otherwise (None, pdf_file)
    """
    pdf_path = os.path.join(pdf_dir, pdf_file)
    # Save Extracted Raw Text
    raw_text_path = get_raw_text_path(pdf_file, text_dir=TEXT_DIR)

    # Check if the raw text file already exists
    if os.path.exists(raw_text_path):
        logging.info(f"Raw text already exists for {pdf_file}. Skipping extraction.")
        # Load the existing raw text since the file already exists
        try:
            with open(raw_text_path, "r", encoding="utf-8") as file:
                raw_text = file.read()
            return raw_text, pdf_file  # Return the loaded raw text

        except Exception as e:
            logging.error(
                f"Error reading raw text from {raw_text_path} for {pdf_file}: {str(e)}"
            )
            return None, pdf_file

    try:
        # Extract Text
        logging.info(f"Extracting text from {pdf_file}")
        raw_text = extract_text_ocr(pdf_path)

        if not raw_text:
            logging.warning(f"No text extracted from {pdf_file}. Skipping...")

            return None, pdf_file  # Skip to the next file if extraction fails

        save_text(raw_text_path, raw_text)
        logging.info(f"Raw text saved for {pdf_file}")

        return raw_text, pdf_file

    except Exception as e:
        logging.error(f"Error text extraction from {pdf_file}: {str(e)}")
        return None, pdf_file
