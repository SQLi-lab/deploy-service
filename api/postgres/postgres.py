import hashlib
import os
import random

import pytz
from datetime import datetime

import psycopg2

from config.config import logger


class DBConnector:
    _postgres = None
    _conn = None

    def __init__(self):
        """
        Метод создания нового подключения к БД Postgres
        """
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER')
        self.POSTGRES_PASS = os.getenv('POSTGRES_PASS')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT')

        if not self.POSTGRES_HOST or not self.POSTGRES_DB or not self.POSTGRES_USER or not self.POSTGRES_PASS or not self.POSTGRES_PORT:
            logger.error(
                'Проверьте наличие и корректность переменных окружения Postgres')
            exit(1)

        if not self._conn:
            try:
                self._conn = psycopg2.connect(
                    host=self.POSTGRES_HOST,
                    database=self.POSTGRES_DB,
                    user=self.POSTGRES_USER,
                    password=self.POSTGRES_PASS,
                    port=self.POSTGRES_PORT
                )
            except Exception as e:
                logger.error(
                    f'Невозможно подключиться к  БД {self.POSTGRES_HOST}:{self.POSTGRES_PORT}')
                exit(1)

            logger.info(
                f"Новое подключение к БД {self.POSTGRES_HOST}:{self.POSTGRES_PORT}")

    def __del__(self):
        """
        Метод очистки соединения и экземпляра БД Postgres
        """
        self.commit()
        self.close_conn()
        self._conn = None
        self._postgres = None

    def get_conn(self):
        """
        Метод получения экземпляра _conn
        """
        if not self._conn:
            self.__init__()

        return self._conn

    def commit(self):
        """
        Метод коммита в БД
        """
        if not self._conn:
            self.__init__()

        self._conn.commit()

    def close_conn(self):
        """
        Метод закрытие существующего соединения
        """
        if self._conn:
            self._conn.close()

    def change_status(self, name: str, uuid: str, status: str) -> bool:
        """
        Метод изменяет статус лабораторной
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        update_query = """
                UPDATE sqli_api_lab
                SET status = %s
                WHERE uuid = %s;
                """

        try:
            cursor.execute(update_query, (status, uuid))
            self.commit()
        except Exception as e:
            logger.error(
                f"[ {name} ]: Ошибка при изменении статуса")
            return False

        cursor.close()
        logger.info(f"[ {name} ]: Статус изменен на '{status}'")
        return True

    def set_date(self, name: str, uuid: str, date_type: str) -> bool:
        """
        Метод зменяет выбранное поле даты, ставит текущую дату
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        tz = pytz.timezone('Europe/Moscow')
        current_date = datetime.now(tz)

        formatted_date = current_date.strftime(
            '%Y-%m-%d %H:%M:%S.%f') + ' ' + current_date.strftime('%z')

        update_query = f"""
                UPDATE sqli_api_lab
                SET {date_type} = %s
                WHERE uuid = %s;
                """

        try:
            cursor.execute(update_query, (formatted_date, uuid))
            self.commit()
        except Exception:
            logger.error(
                f"[ {name} ]: Ошибка при изменении даты {date_type}")
            return False

        cursor.close()
        logger.info(f"[ {name} ]: Дата {date_type} изменена")
        return True

    def set_secret_hash(self, name: str, uuid: str) -> bool or str:
        """
        Метод устанавливает хэш секретного пароля
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        random_number = random.randint(1, 999999)
        secret = f'secret_{hashlib.sha1(str(random_number).encode('utf-8')).hexdigest()}'
        secret_hash = hashlib.sha256(str(secret).encode('utf-8')).hexdigest()

        update_query = """
                UPDATE sqli_api_lab
                SET secret_hash = %s
                WHERE uuid = %s;
                """

        try:
            cursor.execute(update_query, (secret_hash, uuid))
            self.commit()
        except Exception:
            logger.error(
                f"[ {name} ]: Ошибка при установке секретного хэша")
            return False

        cursor.close()
        logger.info(f"[ {name} ]: Секретный хэш установлен")
        return secret_hash
