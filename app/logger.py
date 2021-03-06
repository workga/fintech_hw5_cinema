import logging

from app.config import app_settings


def init_logger() -> None:
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(
        logging.Formatter(
            '%(levelname)s %(asctime)s %(funcName)s(%(lineno)d) %(message)s',
            datefmt='%d/%m/%Y %H:%M:%S',
        )
    )

    logger = logging.getLogger(app_settings.logger_name)
    logger.addHandler(stream_handler)
    logger.setLevel(app_settings.logger_level)


def get_logger() -> logging.Logger:
    return logging.getLogger(app_settings.logger_name)
