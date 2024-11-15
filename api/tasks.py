import time
from datetime import datetime, timedelta

import dramatiq
import requests
from dramatiq.brokers.redis import RedisBroker

from api.ansible import AnsibleApi
from api.postgres import DBConnector
from config.config import REDIS_HOST, REDIS_PORT, logger, WATCHER_URL

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, db=0)
dramatiq.set_broker(redis_broker)

db = DBConnector()
ansible = AnsibleApi()


@dramatiq.actor(max_retries=0)
def create_lab_task(name: str, uuid: str, expired_seconds: str):
    logger.info(f"[ {name} ]: начало запуска лабораторной...")

    ok = db.change_status(name, uuid, 'Создается')
    if not ok:
        return

    secret_hash = db.set_secret_hash(name, uuid)
    if not secret_hash:
        return

    try:
        ansible.start_playbook('lab', uuid)
    except Exception as e:
        ok = db.change_status(name, uuid, 'Ошибка создания')
        if not ok:
            return
        raise Exception(e)

    ok = db.set_url(name, uuid)
    if not ok:
        return

    time.sleep(5)

    ok = db.change_status(name, uuid, 'Выполняется')
    if not ok:
        return

    date, ok = db.set_date(name, uuid, 'date_started')
    if not ok:
        return

    try:
        expired_seconds_int = int(expired_seconds)
        date_started = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f %z")
        date_expired = date_started + timedelta(seconds=expired_seconds_int)
    except Exception as e:
        logger.error(f"[ {name} ]: ошибка формирования даты удлаения")
        return

    logger.info(f"[ {name} ]: будет удалена {date_expired}")

    data = {
        'date': str(date_expired),
        'uuid': str(uuid)
    }

    try:
        response = requests.post(
            f'{WATCHER_URL}/api/v1/add', json=data)
        response.raise_for_status()
    except Exception as e:
        logger.error(f"[ {name} ] ошибка при передаче задачи watcher сервису")
        return

    logger.info(f"[ {name} ]: задача передана сервису watcher")

    logger.info(f"[ {name} ]: лабораторная успешно запущена!")


@dramatiq.actor(max_retries=0)
def delete_lab_task(name: str, uuid: str):
    logger.info(f"[ {name} ]: начало удаления лабораторной...")

    try:
        ansible.start_playbook('lab-delete', uuid)
    except Exception as e:
        ok = db.change_status(name, uuid, 'Ошибка удаления')
        if not ok:
            return
        raise Exception(e)

    ok = db.change_status(name, uuid, 'Остановлена')
    if not ok:
        return

    logger.info(f"[ {name} ]: лабораторная успешно удалена!")
