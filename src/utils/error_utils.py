import logging
from functools import wraps

def handle_errors(log_message="An error occurred"):
    """
    Decorator to handle errors for any function and log the error.

    Args:
        log_message (str): Custom log message to indicate where the error occurred.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.error(f"{log_message} in {func.__name__}: {str(e)}")
                return None
        return wrapper
    return decorator
