import os

import psycopg2

from config.config import logger


class DBConnector:
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_DB = os.getenv('POSTGRES_DB')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASS = os.getenv('POSTGRES_PASS')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')

    _postgres = None
    _conn = None

    def __new__(cls, *args, **kwargs):
        """
        Метод инициализации нового экземпляра БД Postgres
        """
        if not cls.POSTGRES_HOST or not cls.POSTGRES_DB or not cls.POSTGRES_USER or not cls.POSTGRES_PASS or not cls.POSTGRES_PORT:
            logger.warn('Проверьте наличие переменных окружения POSTGRES')
            exit(1)

        if not cls._postgres:
            cls._postgres = super(DBConnector, cls).__new__()

        return object.__new__(cls)

    def __init__(self):
        """
        Метод создания нового подключения к БД Postgres
        """
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
                logger.error(f'Невозможно подключиться к  БД {self.POSTGRES_HOST}:{self.POSTGRES_PORT}')
                exit(1)

            logger.info(f"Новое подключение к БД {self.POSTGRES_HOST}:{self.POSTGRES_PORT}")

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

db = DBConnector()
conn = db.get_conn()
