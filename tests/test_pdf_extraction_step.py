import os
import unittest
from unittest.mock import patch, mock_open
from tempfile import TemporaryDirectory

from src.extract.pdf_extraction_step import pdf_extract

class TestPDFExtraction(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = TemporaryDirectory()
        self.test_dir_path = self.test_dir.name
        self.pdf_file = "test_document.pdf"
        self.raw_text_file = "test_document_raw.txt"

    def tearDown(self):
        # Clean up the temporary directory after each test
        self.test_dir.cleanup()

    @patch('src.extract.pdf_extraction_step.get_raw_text_path')
    @patch('os.path.exists')
    def test_existing_raw_text_file(self, mock_exists, mock_get_raw_text_path):
        # Test if the function correctly handles the case when raw text already exists
        mock_get_raw_text_path.return_value = os.path.join(self.test_dir_path, self.raw_text_file)
        mock_exists.return_value = True

        # Mock opening and reading from the existing raw text file
        with patch('builtins.open', mock_open(read_data="Existing raw text")) as mock_file:
            raw_text, pdf_file = pdf_extract(self.pdf_file, pdf_dir=self.test_dir_path)
            self.assertEqual(raw_text, "Existing raw text")
            self.assertEqual(pdf_file, self.pdf_file)
            mock_file.assert_called_once_with(mock_get_raw_text_path.return_value, 'r', encoding='utf-8')

    @patch('src.extract.pdf_extraction_step.extract_text_ocr')
    @patch('src.extract.pdf_extraction_step.save_text')
    @patch('os.path.exists')
    @patch('src.extract.pdf_extraction_step.get_raw_text_path')
    def test_extract_text_success(self, mock_get_raw_text_path, mock_exists, mock_save_text, mock_extract_text_ocr):
        # Test if the function extracts text from a PDF successfully
        mock_get_raw_text_path.return_value = os.path.join(self.test_dir_path, self.raw_text_file)
        mock_exists.return_value = False
        mock_extract_text_ocr.return_value = "Extracted text content"

        raw_text, pdf_file = pdf_extract(self.pdf_file, pdf_dir=self.test_dir_path)

        self.assertEqual(raw_text, "Extracted text content")
        self.assertEqual(pdf_file, self.pdf_file)
        mock_extract_text_ocr.assert_called_once_with(os.path.join(self.test_dir_path, self.pdf_file))
        mock_save_text.assert_called_once_with(mock_get_raw_text_path.return_value, "Extracted text content")

    @patch('src.extract.pdf_extraction_step.extract_text_ocr')
    @patch('os.path.exists')
    @patch('src.extract.pdf_extraction_step.get_raw_text_path')
    def test_extract_text_failure(self, mock_get_raw_text_path, mock_exists, mock_extract_text_ocr):
        # Test how the function handles the case when extraction fails
        mock_get_raw_text_path.return_value = os.path.join(self.test_dir_path, self.raw_text_file)
        mock_exists.return_value = False
        mock_extract_text_ocr.return_value = None  # Extraction fails

        raw_text, pdf_file = pdf_extract(self.pdf_file, pdf_dir=self.test_dir_path)

        self.assertIsNone(raw_text)
        self.assertEqual(pdf_file, self.pdf_file)
        mock_extract_text_ocr.assert_called_once_with(os.path.join(self.test_dir_path, self.pdf_file))

    @patch('src.extract.pdf_extraction_step.extract_text_ocr')
    @patch('os.path.exists')
    @patch('src.extract.pdf_extraction_step.get_raw_text_path')
    def test_error_handling(self, mock_get_raw_text_path, mock_exists, mock_extract_text_ocr):
        # Test how the function handles exceptions, e.g., file not found
        mock_get_raw_text_path.return_value = os.path.join(self.test_dir_path, self.raw_text_file)
        mock_exists.return_value = False
        mock_extract_text_ocr.side_effect = Exception("Extraction error")

        raw_text, pdf_file = pdf_extract(self.pdf_file, pdf_dir=self.test_dir_path)

        self.assertIsNone(raw_text)
        self.assertEqual(pdf_file, self.pdf_file)
        mock_extract_text_ocr.assert_called_once_with(os.path.join(self.test_dir_path, self.pdf_file))

if __name__ == '__main__':
    unittest.main()
