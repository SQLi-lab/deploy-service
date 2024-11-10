from fastapi import FastAPI
from pydantic import BaseModel
from api.tasks import create_lab_task, delete_lab_task
from config.config import PORT, logger, DEPLOY_SECRET

app = FastAPI()


class RequestLab(BaseModel):
    name: str
    uuid: str  # TODO: убрать и внизу
    deploy_secret: str | None = '7a7caad9b1951db075d508610ae97d87a33e9a33537d9d9604fc035acc084a7d'


@app.post("/lab/add")
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

    create_lab_task.send(data.name, str(data.uuid))

    return {'success': True,
            'message': f'Лабораторная {data.name} принята в обработку'}


@app.delete("/lab/delete")
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

    delete_lab_task.send(data.name, str(data.uuid))

    return {'success': True, 'message': f'Начато удаление {data.name}'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
