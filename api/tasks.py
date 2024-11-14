import time
import dramatiq
from dramatiq.brokers.redis import RedisBroker

from api.ansible import AnsibleApi
from api.postgres import DBConnector
from config.config import REDIS_HOST, REDIS_PORT, logger

redis_broker = RedisBroker(host=REDIS_HOST, port=REDIS_PORT, db=0)
dramatiq.set_broker(redis_broker)

db = DBConnector()
ansible = AnsibleApi()


@dramatiq.actor
def create_lab_task(name: str, uuid: str):
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
        raise Exception(e)

    # TODO: url

    time.sleep(5)

    ok = db.change_status(name, uuid, 'Выполняется')
    if not ok:
        return

    ok = db.set_date(name, uuid, 'date_started')
    if not ok:
        return

    logger.info(f"[ {name} ]: лабораторная успешно запущена!")


@dramatiq.actor
def delete_lab_task(name: str, uuid: str):
    logger.info(f"[ {name} ]: начало удаления лабораторной...")

    ok = ansible.start_playbook('lab-delete', uuid)
    if not ok:
        return

    ok = db.change_status(name, uuid, 'Остановлена')
    if not ok:
        return

    logger.info(f"[ {name} ]: лабораторная успешно удалена!")
