import os
import logging


def setup_logger(logger_name: str, log_file: str):
    """
    Creates and returns a logger with given name and log file
    """

    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate logs
    if logger.handlers:
        return logger

    # Create logs directory if not exists
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # File Handler
    file_handler = logging.FileHandler(log_file, mode="a")
    file_handler.setFormatter(formatter)

    # Console Handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger