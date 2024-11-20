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

# GroqCloud
# API keys
GROQ_API_KEY = "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"

# LLM System Prompt
SYSTEM_PROMPT = """
You are an information extraction assistant. Your task is to extract specific information from the provided text
and return it in a structured JSON format. Follow these instructions closely for the best results.

From the following text, extract the specified information and return it as a JSON object.

Information to extract:
    1. Company Name: The full legal name of the company.
    2. Company Identifier: The company identifier (e.g., registration number) should be extracted as a series of digits only, with no spaces or special characters.
       - For example, if the company identifier is given as "N° d'entreprise: 123 456 789", you should extract it as "123456789".
   3. Document Purpose: Include all relevant and important fields about the document purpose from the text under the 'Document Purpose' section.
        - Each piece of information should be included as a separate key within the 'Document Purpose' key.

Output Requirements:
    - Return only the JSON object with no additional text or explanations.
    - Ensure the JSON object is well-formatted and complete.
    - The Company Identifier should only contain digits tied without spacing or other symbols.
    - **All keys in the JSON response must always be in English.**
"""