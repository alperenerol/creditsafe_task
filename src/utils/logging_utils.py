import os
import logging


def setup_logging(log_file=None, level=logging.INFO, console=True):
    """
    Sets up logging for the application.

    Args:
        log_file (str): Optional path to the log file where logs should be saved.
        level (int): The logging level (e.g., logging.INFO, logging.DEBUG).
        console (bool): Whether to also print logs to the console (default is True).
    """
    # Define the logging format
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    # Get the root logger
    logger = logging.getLogger()
    logger.setLevel(level)

    # Ensure no duplicate handlers are added
    if not logger.handlers:
        # File Handler (if log_file is provided)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(
                logging.Formatter(log_format, datefmt=date_format)
            )
            logger.addHandler(file_handler)

        # Console Handler (if console output is desired)
        if console:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(level)
            console_handler.setFormatter(
                logging.Formatter(log_format, datefmt=date_format)
            )
            logger.addHandler(console_handler)


def reset_logging():
    logging.info(f"Program execution completed successfully.")
    logging.shutdown()
    # Retrieve and close each handler, ensuring resources are released
    handlers = logging.root.handlers[:]
    for handler in handlers:
        handler.close()
        logging.root.removeHandler(handler)
        handler = None
