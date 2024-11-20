import os
import unittest
from unittest.mock import patch, mock_open
from tempfile import TemporaryDirectory

from src.preprocess.preprocessing_step import raw_text_preprocess

class TestTextPreprocessing(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = TemporaryDirectory()
        self.test_dir_path = self.test_dir.name
        self.pdf_file = "test_document.pdf"
        self.raw_text_content = "This is some raw text content."
        self.preprocessed_text_content = "This is the preprocessed text content."

    def tearDown(self):
        # Clean up the temporary directory after each test
        self.test_dir.cleanup()

    @patch('src.preprocess.preprocessing_step.get_preprocessed_text_path')
    @patch('os.path.exists')
    def test_preprocessed_file_exists(self, mock_exists, mock_get_preprocessed_text_path):
        # Test if the function correctly handles the case when preprocessed text already exists
        preprocessed_text_path = os.path.join(self.test_dir_path, "test_document_preprocessed.txt")
        mock_get_preprocessed_text_path.return_value = preprocessed_text_path
        mock_exists.return_value = True

        # Mock opening and reading from the existing preprocessed text file
        with patch('builtins.open', mock_open(read_data=self.preprocessed_text_content)) as mock_file:
            preprocessed_text = raw_text_preprocess(self.raw_text_content, self.pdf_file, text_dir=self.test_dir_path)
            self.assertEqual(preprocessed_text, self.preprocessed_text_content)
            mock_file.assert_called_once_with(preprocessed_text_path, 'r', encoding='utf-8')

    @patch('src.preprocess.preprocessing_step.process_text')
    @patch('src.preprocess.preprocessing_step.save_text')
    @patch('os.path.exists')
    @patch('src.preprocess.preprocessing_step.get_preprocessed_text_path')
    def test_successful_preprocessing(self, mock_get_preprocessed_text_path, mock_exists, mock_save_text, mock_process_text):
        # Test if the function preprocesses the text successfully
        preprocessed_text_path = os.path.join(self.test_dir_path, "test_document_preprocessed.txt")
        mock_get_preprocessed_text_path.return_value = preprocessed_text_path
        mock_exists.return_value = False
        mock_process_text.return_value = self.preprocessed_text_content

        preprocessed_text = raw_text_preprocess(self.raw_text_content, self.pdf_file, text_dir=self.test_dir_path)

        self.assertEqual(preprocessed_text, self.preprocessed_text_content)
        mock_process_text.assert_called_once_with(self.raw_text_content)
        mock_save_text.assert_called_once_with(preprocessed_text_path, self.preprocessed_text_content)

    @patch('src.preprocess.preprocessing_step.process_text')
    @patch('os.path.exists')
    @patch('src.preprocess.preprocessing_step.get_preprocessed_text_path')
    def test_preprocessing_failure(self, mock_get_preprocessed_text_path, mock_exists, mock_process_text):
        # Test how the function handles the case when preprocessing fails
        preprocessed_text_path = os.path.join(self.test_dir_path, "test_document_preprocessed.txt")
        mock_get_preprocessed_text_path.return_value = preprocessed_text_path
        mock_exists.return_value = False
        mock_process_text.return_value = None  # Preprocessing fails

        preprocessed_text = raw_text_preprocess(self.raw_text_content, self.pdf_file, text_dir=self.test_dir_path)

        self.assertIsNone(preprocessed_text)
        mock_process_text.assert_called_once_with(self.raw_text_content)

    @patch('src.preprocess.preprocessing_step.process_text')
    @patch('os.path.exists')
    @patch('src.preprocess.preprocessing_step.get_preprocessed_text_path')
    def test_error_handling(self, mock_get_preprocessed_text_path, mock_exists, mock_process_text):
        # Test how the function handles exceptions, e.g., during saving the text
        preprocessed_text_path = os.path.join(self.test_dir_path, "test_document_preprocessed.txt")
        mock_get_preprocessed_text_path.return_value = preprocessed_text_path
        mock_exists.return_value = False
        mock_process_text.side_effect = Exception("Processing error")

        preprocessed_text = raw_text_preprocess(self.raw_text_content, self.pdf_file, text_dir=self.test_dir_path)

        self.assertIsNone(preprocessed_text)
        mock_process_text.assert_called_once_with(self.raw_text_content)

if __name__ == '__main__':
    unittest.main()
