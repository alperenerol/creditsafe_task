from src.utils.error_utils import handle_errors
from pdf2image import convert_from_path
import pytesseract
import cv2
import numpy as np

@handle_errors(log_message="Error during text extraction")
def extract_text(pdf_path):
    """
    Extracts text from a PDF file by converting each page to an image and using OCR.

    Args:
        pdf_path (str): The path to the PDF file.
    
    Returns:
        str: The extracted text from the PDF.
    """
    extracted_text = ""

    try:
        # Convert PDF to images (one image per page)
        images = convert_from_path(pdf_path, dpi=400)

        # Iterate through each page image and perform OCR
        for page_number, image in enumerate(images, start=1):
            # Convert PIL image to a NumPy array
            img = np.array(image)

            # Convert to grayscale for better OCR accuracy
            gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

            # Apply thresholding to improve text clarity for OCR
            thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 4) # c=6, dpi=400 optimal for pdf5-10

            # Perform OCR on the thresholded image
            text = pytesseract.image_to_string(thresh)  # Add 'lang' to specify the language

            # Add the page number and extracted text to the final text output
            extracted_text += f"--- Page {page_number} ---\n{text}\n"

    except Exception as e:
        # Log and re-raise the exception to handle it with the decorator
        raise RuntimeError(f"Failed to extract text from {pdf_path}: {str(e)}")

    return extracted_text
    