import logging
import os

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


def init_logger() -> logging.Logger:
    """
    Функция создает логгер для консоли и файла
    :return: логгер
    """
    log_format = logging.Formatter("%(asctime)s [%(levelname)s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    file_handler = logging.FileHandler("log/deploy-service.log")
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger

logger = init_logger()
PORT = int(os.getenv('PORT', 8001))

CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
if CELERY_BROKER_URL is None:
    error = "Переменная окружения CELERY_BROKER_URL не установлена"
    logger.error(error)
    raise ValueError(error)