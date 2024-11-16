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
WATCHER_URL = os.getenv('WATCHER_URL', 'http://watcher:8002')
DEPLOY_SECRET = os.getenv("DEPLOY_SECRET")

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


ANSIBLE_TIMEOUT = int(os.getenv('ANSIBLE_TIMEOUT', 600))
ANSIBLE_PLAYBOOKS_DIR = os.getenv('ANSIBLE_PLAYBOOKS_DIR', "/app/ansible")
if not ANSIBLE_PLAYBOOKS_DIR:
    logger.error('Проверьте наличие и правильность переменной окружения ANSIBLE_PLAYBOOKS_DIR')
    exit(1)
