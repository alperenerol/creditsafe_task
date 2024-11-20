import unittest
import os
import json
from tempfile import TemporaryDirectory

from src.utils.file_utils import (
    save_text,
    save_json,
    get_raw_text_path,
    get_preprocessed_text_path,
)


class TestFileUtils(unittest.TestCase):

    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = TemporaryDirectory()
        self.test_dir_path = self.test_dir.name

    def tearDown(self):
        # Clean up the temporary directory after each test
        self.test_dir.cleanup()

    def test_save_text(self):
        # Test if save_text saves content correctly
        test_file = os.path.join(self.test_dir_path, "test_text.txt")
        test_content = "This is a test content."

        save_text(test_file, test_content)

        # Verify that the file was created and contains the correct content
        with open(test_file, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content, test_content)

    def test_save_json_create_new(self):
        # Test if save_json creates a new JSON file
        test_file = os.path.join(self.test_dir_path, "test.json")
        new_data = {"key": "value"}

        save_json(test_file, new_data)

        # Verify that the file was created and contains the correct data
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [new_data])

    def test_save_json_append(self):
        # Test if save_json appends data to an existing JSON file
        test_file = os.path.join(self.test_dir_path, "test_append.json")
        initial_data = {"key1": "value1"}
        new_data = {"key2": "value2"}

        # Create the initial JSON file
        save_json(test_file, initial_data)

        # Append new data
        save_json(test_file, new_data)

        # Verify that the file contains both entries
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [initial_data, new_data])

    def test_save_json_invalid_file(self):
        # Test if save_json handles an invalid JSON file gracefully
        test_file = os.path.join(self.test_dir_path, "invalid.json")

        # Create an invalid JSON file
        with open(test_file, "w", encoding="utf-8") as f:
            f.write("INVALID JSON CONTENT")

        # Attempt to append new data to the invalid JSON file
        new_data = {"key": "value"}
        save_json(test_file, new_data)

        # Verify that the invalid file was replaced with the new data
        with open(test_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data, [new_data])

    def test_get_raw_text_path(self):
        # Test if get_raw_text_path returns the correct path
        pdf_file = "test_document.pdf"
        expected_path = os.path.join(self.test_dir_path, "test_document_raw.txt")

        # Call get_raw_text_path with the test directory
        result = get_raw_text_path(pdf_file, text_dir=self.test_dir_path)
        self.assertEqual(result, expected_path)

    def test_get_preprocessed_text_path(self):
        # Test if get_preprocessed_text_path returns the correct path
        pdf_file = "test_document.pdf"
        expected_path = os.path.join(
            self.test_dir_path, "test_document_preprocessed.txt"
        )

        # Call get_preprocessed_text_path with the test directory
        result = get_preprocessed_text_path(pdf_file, text_dir=self.test_dir_path)
        self.assertEqual(result, expected_path)


if __name__ == "__main__":
    unittest.main()
