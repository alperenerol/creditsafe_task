import re

from src.utils.error_utils import handle_errors


@handle_errors(log_message="Error during text preprocessing")
def process_text(text):
    """
    Preprocesses the extracted text by applying various cleaning and formatting steps.

    Args:
        text (str): The raw extracted text.

    Returns:
        str: The cleaned and preprocessed text.
    """

    # Step 1: Remove Garbled Text and Noise
    text = remove_garbled_text(text)

    # Step 2: Fix Common OCR Errors
    text = fix_common_ocr_errors(text)

    # Step 3: Normalize Whitespaces
    text = normalize_whitespaces(text)

    return text


# Normalize Whitespaces
def normalize_whitespaces(text):
    # Replace multiple spaces and tabs with a single space
    return re.sub(r"\s+", " ", text).strip()


# Remove Garbled Text and Noise
def remove_garbled_text(text):
    # Remove sequences of random, repeated characters or meaningless text
    # Remove sequences of repeated characters (letters/numbers) with no structure
    text = re.sub(
        r"\b\w{1,2}(\s+\w{1,3}){4,6}\b", "", text
    )  # Repeated short words or letters

    return text


# Fix Common OCR Errors
def fix_common_ocr_errors(text):
    # Correct errors in Company Identifier
    text = re.sub(
        r"\bN° centreprise\b", "N° d'entreprise", text
    )  # Fix "centreprise" to "d'entreprise"
    text = re.sub(
        r"\bN° dentraprise\b", "N° d'entreprise", text
    )  # Fix "dentraprise" to "d'entreprise"
    text = re.sub(
        r"\bwe dentreprise\b", "N° d'entreprise", text
    )  # Fix "we dentreprise" typo
    text = re.sub(r"\bNow\b", "Nom", text)  # Correct "Now" to "Nom"

    # Correct errors in Company Name and related fields
    text = re.sub(
        r"\bfen entier\b", "(en entier)", text
    )  # Fix "fen entier" to "(en entier)"
    text = re.sub(
        r"\bfen abrégé\b", "(en abrégé)", text
    )  # Fix "fen abrégé" to "(en abrégé)"
    text = re.sub(
        r"\bfenentiey\b", "(en entier)", text
    )  # Correct further variant "fenentiey"
    text = re.sub(r"\bfen enter\b", "(en entier)", text)  # Fix variant "fen enter"
    text = re.sub(r"\bfan entier\b", "(en entier)", text)  # Fix variant "fan entier"
    text = re.sub(r"\bfan abrégé\b", "(en abrégé)", text)  # Fix variant "fan abrégé"

    # Correct errors in Document Purpose
    text = re.sub(
        r"\bObjet de Pacte\b", "Objet de l'acte", text
    )  # Fix "Objet de Pacte" to "Objet de l'acte"
    text = re.sub(
        r"\bObiet de 'acte\b", "Objet de l'acte", text
    )  # Correct missing "l'" apostrophe
    text = re.sub(r"\bObiet\b", "Objet", text)  # Fix "Obiet" to "Objet"
    text = re.sub(r"\bOblet\b", "Objet", text)  # Fix further misspellings of "Objet"
    return text
