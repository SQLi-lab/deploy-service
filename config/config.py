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

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger


logger = init_logger()
PORT = int(os.getenv('PORT', 8001))
BACKEND_URL = os.getenv('BACKEND_URL', 'http://sqli_lab:8000')
TIMEOUT = int(os.getenv('TIMEOUT', 60))
DEPLOY_SECRET = '7a7caad9b1951db075d508610ae97d87a33e9a33537d9d9604fc035acc084a7d'

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


ANSIBLE_TIMEOUT = int(os.getenv('ANSIBLE_TIMEOUT', 600))
ANSIBLE_PLAYBOOKS_DIR = os.getenv('ANSIBLE_PLAYBOOKS_DIR')
if not ANSIBLE_PLAYBOOKS_DIR:
    logger.error('Проверьте наличие и правильность переменной окружения ANSIBLE_PLAYBOOKS_DIR')
    exit(1)
