import random

import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker
from datetime import datetime, timedelta
from api.ansible import AnsibleApi
from api.postgres import DBConnector
from config.config import REDIS_HOST, REDIS_PORT, logger, WATCHER_URL, \
    VARIANT_MAP, NUM_OF_VARIANTS

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, db=0)
dramatiq.set_broker(redis_broker)

db = DBConnector()
ansible = AnsibleApi()


@dramatiq.actor(max_retries=0)
def create_lab_task(uuid: str, expired_seconds: str):
    """
    Отложенная задача запуска лабораторной
    :param uuid: uuid лабораторной
    :param expired_seconds: время на выполнение в секундах
    """
    logger.info(f"[ {uuid} ]: начало запуска лабораторной...")

    ok = db.change_status(uuid, 'Создается')
    if not ok:
        return

    secret_hash = db.set_secret_hash(uuid) # получение хэш части секрета secret_{secret_hash}
    if not secret_hash:
        return

    random_variant = random.randint(1, NUM_OF_VARIANTS)
    variant_name = VARIANT_MAP[random_variant]

    logger.info(f"[ {uuid} ]: использован вариант <{variant_name}>")

    try:
        db.upload_variant(uuid, secret_hash, variant_name) # заполенние БД данными
        ansible.start_playbook(variant_name, uuid) # запуск контейнеров с лабами
    except Exception as e:
        ok = db.change_status(uuid, 'Ошибка создания')
        if not ok:
            return
        raise Exception(e)

    ok = db.set_url(uuid)
    if not ok:
        return

    ok = db.change_status(uuid, 'Выполняется')
    if not ok:
        return

    date, ok = db.set_date(uuid, 'date_started')
    if not ok:
        return

    # вычисление даты удаления
    try:
        expired_seconds_int = int(expired_seconds)
        date_started = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f %z")
        date_expired = date_started + timedelta(seconds=expired_seconds_int)
    except Exception as e:
        logger.error(f"[ {uuid} ]: ошибка формирования даты удлаения")
        return

    logger.info(f"[ {uuid} ]: будет удалена {date_expired}")

    data = {
        'date': str(date_expired),
        'uuid': str(uuid)
    }

    try:
        response = requests.post(
            f'{WATCHER_URL}/api/v1/add', json=data)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"[ {uuid} ] ошибка при передаче задачи watcher сервису")
        return

    logger.info(f"[ {uuid} ]: задача передана сервису watcher")

    logger.info(f"[ {uuid} ]: лабораторная успешно запущена!")


@dramatiq.actor(max_retries=0)
def delete_lab_task(uuid: str):
    """
    Отложенная задача на удаление лабораторной
    :param uuid: uuid лабораторной
    """
    logger.info(f"[ {uuid} ]: начало удаления лабораторной...")

    try:
        ansible.start_playbook('lab-delete', uuid)
    except Exception as e:
        ok = db.change_status(uuid, 'Ошибка удаления')
        if not ok:
            return
        raise Exception(e)

    ok = db.change_status(uuid, 'Остановлена')
    if not ok:
        return

    ok = db.drop_database(uuid)
    if not ok:
        return

    logger.info(f"[ {uuid} ]: лабораторная успешно удалена!")
