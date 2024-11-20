import unittest
from unittest.mock import patch
import json
from tempfile import TemporaryDirectory

from config import SYSTEM_PROMPT
from src.inference.inference_step import perform_inference

class TestInference(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = TemporaryDirectory()
        self.test_dir_path = self.test_dir.name
        self.pdf_file = "test_document.pdf"
        self.preprocessed_text = "This is some preprocessed text content."
        self.valid_response = json.dumps({"key": "value"})

    def tearDown(self):
        # Clean up the temporary directory after each test
        self.test_dir.cleanup()

    @patch('src.inference.inference_step.generate_response')
    @patch('src.inference.inference_step.save_json')
    @patch('os.path.join', return_value='/tmp/output.json')
    def test_successful_inference(self, mock_path_join, mock_save_json, mock_generate_response):
        # Mock a successful response from the LLM
        mock_generate_response.return_value = self.valid_response

        # Run the inference function
        perform_inference(self.preprocessed_text, self.pdf_file)

        # Verify that generate_response was called with the expected messages
        expected_messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": self.preprocessed_text}
        ]
        mock_generate_response.assert_called_once_with(expected_messages)

        # Verify that save_json was called with the correct data
        expected_output = json.loads(self.valid_response)
        expected_output.update({"file_name": self.pdf_file})
        mock_save_json.assert_called_once_with('/tmp/output.json', expected_output)

    @patch('src.inference.inference_step.generate_response')
    def test_empty_response(self, mock_generate_response):
        # Mock an empty response from the LLM
        mock_generate_response.return_value = ""

        # Run the inference function
        result = perform_inference(self.preprocessed_text, self.pdf_file)

        # Verify that the function returns False to indicate an empty response was handled
        self.assertFalse(result)

    @patch('src.inference.inference_step.generate_response')
    @patch('src.inference.inference_step.logging.error')
    def test_invalid_json_response(self, mock_logging_error, mock_generate_response):
        # Mock an invalid JSON response from the LLM
        mock_generate_response.return_value = "Invalid JSON response"

        # Run the inference function
        perform_inference(self.preprocessed_text, self.pdf_file)

        # Verify that an error was logged for the JSON decoding issue
        mock_logging_error.assert_any_call(f"Error decoding JSON for {self.pdf_file}: Expecting value: line 1 column 1 (char 0).")

    @patch('src.inference.inference_step.generate_response')
    @patch('src.inference.inference_step.logging.error')
    def test_exception_handling(self, mock_logging_error, mock_generate_response):
        # Mock generate_response to raise an exception
        mock_generate_response.side_effect = Exception("Unexpected error")

        # Run the inference function
        perform_inference(self.preprocessed_text, self.pdf_file)

        # Verify that an error was logged for the exception
        mock_logging_error.assert_called_once_with(f"Error generating response from LLM: Unexpected error")

if __name__ == '__main__':
    unittest.main()
