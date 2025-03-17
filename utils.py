import re
import logging
from constants import APPLICATION_NAME


def setup_logging():
    """
    Set up the root logger with file and console handlers.
    """
    # Create a logger
    logger = logging.getLogger(APPLICATION_NAME)
    logger.setLevel(logging.DEBUG)  # Set the base logging level

    # Create a file handler
    file_handler = logging.FileHandler(f"{APPLICATION_NAME}.log")
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  # Only log INFO and above to the console

    # Create a formatter and add it to the handlers
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


def clean_text(text):
    # Remove ANSI escape codes using regex
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    cleaned_text = ansi_escape.sub("", text)

    # Replace \r\n and \n\r with \n for consistent line breaks
    cleaned_text = cleaned_text.replace("\r\n", "\n").replace("\n\r", "\n")

    # Remove trailing and leading whitespace
    cleaned_text = cleaned_text.strip()

    return cleaned_text
