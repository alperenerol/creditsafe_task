import re
from src.utils.error_utils import handle_errors

@handle_errors(log_message="Error during text preprocessing")
def preprocess_text(text):
    """
    Preprocesses the extracted text by applying various cleaning and formatting steps.

    Args:
        text (str): The raw extracted text.

    Returns:
        str: The cleaned and preprocessed text.
    """
    # Step 1: Normalize Whitespaces
    text = normalize_whitespaces(text)

    # Step 2: Correct Punctuation Spacing
    text = fix_punctuation_spacing(text)

    # Step 3: Remove Special Characters (excluding common punctuation)
    text = remove_special_characters(text)

    # Step 4: Clean Unnecessary Lines
    text = clean_unnecessary_lines(text)

    return text

# Step 1: Normalize Whitespaces
def normalize_whitespaces(text):
    # Replace multiple spaces and tabs with a single space
    return re.sub(r'\s+', ' ', text).strip()

# Step 2: Correct Punctuation Spacing
def fix_punctuation_spacing(text):
    # Remove spaces before punctuation and ensure a single space after punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)  # Remove space before punctuation
    text = re.sub(r"([.,;:!?])(\w)", r"\1 \2", text)  # Ensure space after punctuation if needed
    return text

# Step 3: Remove Special Characters (keep common punctuation and alphanumeric characters)
def remove_special_characters(text):
    # Remove any character that is not a word character, space, or common punctuation
    return re.sub(r'[^\w\s.,!?;:]', '', text)

# Step 4: Clean Unnecessary Lines
def clean_unnecessary_lines(text):
    # Remove lines that consist only of non-alphanumeric characters or whitespace
    text = re.sub(r'^[^a-zA-Z0-9]+$', "", text, flags=re.MULTILINE)
    # Remove excessive empty lines
    text = re.sub(r'\n{2,}', '\n\n', text)
    return text