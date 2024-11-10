import uuid
from fastapi import FastAPI
from pydantic import BaseModel

from api.deploy.deploy import delete_lab_task, create_lab_task
from config.config import PORT, logger

app = FastAPI()


class RequestLab(BaseModel):
    name: str
    uuid: uuid.UUID


@app.post("/lab/add")
async def create_lab(data: RequestLab):
    """
    Ручка для запроса развертывнаия лабораторной
    :param data: json с uuid
    :return: json ответ message и success
    """
    logger.info(f"Запрос на создание: {data.name}")

    create_lab_task.delay(data.name, data.uuid)

    return {'success': True, 'message': f'Лабораторная {data.name} принята в обработку'}


@app.delete("/lab/delete")
async def delete_lab(data: RequestLab):
    """
    Ручка для запроса удаления лабораторной
    :param data: json с uuid
    :return: json ответ message и success
    """
    logger.info(f"Запрос на удаление: {data.name}")

    delete_lab_task.delay(data.name, data.uuid)

    return {'success': True, 'message': f'Начато удаление {data.name}'}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=PORT)
