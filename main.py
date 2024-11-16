import redis.exceptions
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from api.tasks import create_lab_task, delete_lab_task
from config.config import PORT, logger, DEPLOY_SECRET

app = FastAPI()

api_v1 = APIRouter(prefix="/api/v1", tags=["v1"])


class RequestLab(BaseModel):
    name: str
    uuid: str
    expired_seconds: str
    deploy_secret: str | None = '7a7caad9b1951db075d508610ae97d87a33e9a33537d9d9604fc035acc084a7d'  # TODO: убрать


@api_v1.post("/lab/add")
async def create_lab(data: RequestLab):
    """
    Ручка для запроса развертывнаия лабораторной
    :param data: json с uuid
    :return: json ответ message и success
    """
    logger.info(f"Запрос на создание: {data.name}")

    if data.deploy_secret != DEPLOY_SECRET:
        return {'success': False,
                'message': f'Неавторизованный доступ'}

    try:
        create_lab_task.send(str(data.uuid), str(data.expired_seconds))
    except redis.exceptions.ConnectionError:
        return {'success': False,
                'message': 'Ошибка передачи лабораторной на запуск'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

    return {'success': True,
            'message': f'Лабораторная {data.name} принята в обработку'}


@api_v1.delete("/lab/delete")
async def delete_lab(data: RequestLab):
    """
    Ручка для запроса удаления лабораторной
    :param data: json с uuid
    :return: json ответ message и success
    """
    logger.info(f"Запрос на удаление: {data.name}")

    if data.deploy_secret != DEPLOY_SECRET:
        return {'success': False,
                'message': f'Неавторизованный доступ'}

    try:
        delete_lab_task.send(str(data.uuid))
    except redis.exceptions.ConnectionError:
        return {'success': False,
                'message': 'Ошибка передачи лабораторной на запуск'}
    except Exception as e:
        return {'success': False, 'message': str(e)}

    return {'success': True, 'message': f'Начато удаление {data.name}'}


app.include_router(api_v1)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
