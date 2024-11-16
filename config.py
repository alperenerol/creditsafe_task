import os

try:
    # Get the directory of the current script file (works when running from a file)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except NameError:
    # Get the current working directory (works in an interactive environment)
    BASE_DIR = os.getcwd()

# Directory for storing input PDF files
PDF_DIR = os.path.join(BASE_DIR, 'data', 'pdfs', 'BE_GAZETTE_PDFS')

# Directory for storing preprocessed text files
TEXT_DIR = os.path.join(BASE_DIR, 'data', 'text')

# Directory for storing final output JSON files
OUTPUT_DIR = os.path.join(BASE_DIR, 'data', 'outputs')

# Other configurations (optional)
LOG_DIR = os.path.join(BASE_DIR, 'logs')
LOG_FILE = os.path.join(LOG_DIR, 'process.log')

# API keys
GROQ_API_KEY = "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"