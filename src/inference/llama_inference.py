import logging
from config import GROQ_API_KEY
from src.utils.error_utils import handle_errors
from groq import Groq

@handle_errors(log_message="Error during response generation")
def generate_response(messages):
    """
    Generates a response using the Groq's Llama 3.1 model.

    Args:
        messages (list): A list of message dictionaries containing user prompts for the model.

    Returns:
        str: The generated response from the model.
    """

    # Create the Groq client using the API key from the config file
    client = Groq(api_key=GROQ_API_KEY)

    try:
        # Create a completion request with the messages
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Specify the model you want to use
            messages=messages,
            temperature=0.2,           # Adjust temperature for response creativity (lower means more focused)
            max_tokens=1000,            # Adjust maximum tokens in response
            top_p=1.0,                 # Top-p sampling for response diversity
            stream=False               # No streaming, simple response generation
)

        # Collect the chunks from the stream and return the final response
        response_text = response.choices[0].message.content

        return response_text

    except Exception as e:
        logging.error(f"Error occurred while generating response: {e}")
        return "Sorry, an error occurred while generating the response."