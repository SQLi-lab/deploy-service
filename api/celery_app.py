from celery import Celery

from config.config import CELERY_BROKER_URL


celery_app = Celery(
    "tasks",
    broker=CELERY_BROKER_URL
)


celery_app.conf.update(
    worker_hijack_root_logger=False,
    broker_connection_retry_on_startup=True,
)
# Автозагрузка задач из указанного пути
celery_app.autodiscover_tasks(['api.deploy.deploy'])

