import logging
from constants import APPLICATION_NAME


def setup_logging(name=APPLICATION_NAME):
    """
    Set up the root logger with file and console handlers.
    """
    # Create a logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set the base logging level

    # Create a file handler
    file_handler = logging.FileHandler(f"{APPLICATION_NAME}.log")
    file_handler.setLevel(logging.DEBUG)  # Log everything to the file

    # Create a console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)  # Only log INFO and above to the console

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
