import os
import logging
from concurrent.futures import ProcessPoolExecutor
from concurrent.futures import as_completed

from config import PDF_DIR, TEXT_DIR, LOG_FILE
from src.extract.pdf_extraction_step import pdf_extract
from src.preprocess.preprocessing_step import raw_text_preprocess
from src.inference.inference_step import perform_inference
from src.utils.logging_utils import setup_logging, reset_logging

# Set up logging
setup_logging(log_file=LOG_FILE, level=logging.INFO, console=True)


def execute_workflow():
    # Step 1: Extract Text and Preprocess
    logging.info("Starting OCR text extraction from PDFs...")

    # Get list of all PDF files
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]

    # Use ProcessPoolExecutor for parallel PDF extraction
    max_workers = int(0.3 * os.cpu_count())
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        # Submit each task individually using executor.submit for finer control
        futures = [executor.submit(pdf_extract, pdf_file) for pdf_file in pdf_files]

        # Use as_completed to process results as they complete
        for future in as_completed(futures):
            try:
                raw_text, pdf_file = (
                    future.result()
                )  # Get the result of the completed task
                if raw_text:
                    # Preprocess Text
                    preprocessed_text = raw_text_preprocess(
                        raw_text, pdf_file, TEXT_DIR
                    )
                    if preprocessed_text:
                        # Perform LLM Inference
                        perform_inference(preprocessed_text, pdf_file)

            except Exception as e:
                logging.error(f"Error during parallel processing: {e}")


if __name__ == "__main__":
    execute_workflow()
    reset_logging()
