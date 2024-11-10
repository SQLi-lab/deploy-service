import time
import uuid

from celery import shared_task

from api.celery_app import celery_app
from config.config import logger


@shared_task
def create_lab_task(name: str, uuid: uuid.UUID):
    logger.info(f"[ {name} ]: начало запуска лабораторной...")
    time.sleep(5)
    logger.info(f"[ {name} ]: лабораторная успешно запущена!")


@shared_task
def delete_lab_task(name:str, uuid: uuid.UUID):
    logger.info(f"[ {name} ]: начало удаления лабораторной...")
    time.sleep(5)
    logger.info(f"[ {name} ]: лабораторная успешно удалена!")
