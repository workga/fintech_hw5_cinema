import logging

from app.config import LOGGER_LEVEL, LOGGER_NAME


def init_logger() -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(
            '%(levelname)s %(asctime)s %(funcName)s(%(lineno)d) %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    )

    logger = logging.getLogger(LOGGER_NAME)
    logger.addHandler(stream_handler)
    logger.setLevel(LOGGER_LEVEL)


def get_logger() -> logging.Logger:
    return logging.getLogger(LOGGER_NAME)
