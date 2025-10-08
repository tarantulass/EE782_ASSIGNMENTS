import logging
import os

def get_logger(name: str):
    # make logs directory
    os.makedirs("logs", exist_ok=True)
    log_file = os.path.join(
        "logs", f"{name}.log"
    )

    # configure logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # avoid duplicate handlers
    if not logger.handlers:
        file_handler = logging.FileHandler(log_file)
        stream_handler = logging.StreamHandler()

        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

    return logger
