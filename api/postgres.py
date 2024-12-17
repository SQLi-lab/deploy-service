import hashlib
import os
import random
import psycopg2
import pytz
from datetime import datetime
from config.config import logger
from api.generator.source.generator import main_generation


class DBConnector:
    _postgres = None
    _conn = None

    def __init__(self):
        """
        Метод создания нового подключения к БД Postgres
        """
        self.POSTGRES_HOST = os.getenv('POSTGRES_HOST')
        self.POSTGRES_USER = os.getenv('POSTGRES_USER')
        self.POSTGRES_PASS = os.getenv('POSTGRES_PASS')
        self.POSTGRES_PORT = os.getenv('POSTGRES_PORT')
        self.POSTGRES_DB = os.getenv('POSTGRES_DB')

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
        if not self._conn or self._conn.closed:
            logger.info(
                "Соединение отсутствует или закрыто. Попытка восстановления...")
            try:
                self._conn = psycopg2.connect(
                    host=self.POSTGRES_HOST,
                    database=self.POSTGRES_DB,
                    user=self.POSTGRES_USER,
                    password=self.POSTGRES_PASS,
                    port=self.POSTGRES_PORT
                )
                logger.info("Соединение успешно восстановлено.")
            except Exception as e:
                logger.error(f"Ошибка восстановления соединения: {e}")
                raise e

        return self._conn

    def get_lab_conn(self, database_name):
        """
        Метод создает и возвращает подключение к Database лабораторной
        """
        self._conn = psycopg2.connect(
            host=self.POSTGRES_HOST,
            database=database_name,
            user=self.POSTGRES_USER,
            password=self.POSTGRES_PASS,
            port=self.POSTGRES_PORT
        )
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
        self._conn = None

    def change_status(self, uuid: str, status: str) -> bool:
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
        except Exception:
            logger.error(
                f"[ {uuid} ]: Ошибка при изменении статуса. Проверьте правильность uuid.")
            return False

        cursor.close()
        logger.info(f"[ {uuid} ]: Статус изменен на '{status}'")
        return True

    def set_url(self, uuid: str) -> bool:
        """
        Метод устанавливает ссылку на выполнение лабораторной работы
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        update_query = f"""
                        UPDATE sqli_api_lab
                        SET url = %s
                        WHERE uuid = %s;
                        """

        try:
            cursor.execute(update_query, (f'/away/{uuid}', uuid))
            self.commit()
        except Exception:
            logger.error(
                f"[ {uuid} ]: Ошибка при установлении URL")
            return False

        cursor.close()
        logger.info(f"[ {uuid} ]: URL установлен")
        return True

    def set_date(self, uuid: str, date_type: str) -> (str, bool):
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
                f"[ {uuid} ]: Ошибка при изменении даты {date_type}")
            return formatted_date, False

        cursor.close()
        logger.info(f"[ {uuid} ]: Дата {date_type} изменена")
        return formatted_date, True

    def set_secret_hash(self, uuid: str) -> bool or str:
        """
        Метод устанавливает хэш секретного пароля
        """
        conn = self.get_conn()
        cursor = conn.cursor()

        random_number = random.randint(1, 999999)
        secret_in_hash = hashlib.sha1(
            str(random_number).encode('utf-8')).hexdigest()[:-1]
        secret = f'secret_{secret_in_hash}'
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
                f"[ {uuid} ]: Ошибка при установке секретного хэша")
            return False

        cursor.close()
        logger.info(f"[ {uuid} ]: Секретный хэш установлен")
        return secret_in_hash

    def upload_variant(self, uuid, secret: str, variant: str):
        """
        Метод создает и заполняет таблицу лабораторной данными
        """
        generator_config = {
            "target_area": variant,
            "uuid": uuid,
            "secrets": [
                f"ibks1_{{{secret[0:13]}}}",
                f"ibks2_{{{secret[13:26]}}}",
                f"ibks3_{{{secret[26:]}}}"
            ],
            "number_extra_tables": 10,
            "noise_flag": False,
            "anonym_flag": False,
            "target_language": "ru"
        }

        structure_sql, data_sql = main_generation(generator_config)
        database_name = uuid.replace("-", "_")

        conn = self.get_conn()
        conn.autocommit = True
        cursor = conn.cursor()

        db_create_query_drop = f"""
                        DROP DATABASE IF EXISTS "{database_name}";
                        """
        db_create_query_create = f"""
                        CREATE DATABASE "{database_name}";
                        """

        try:
            cursor.execute(db_create_query_drop)
            cursor.execute(db_create_query_create)
            self.commit()
        except Exception:
            logger.error(
                f"[ {uuid} ]: Ошибка при создании таблицы для лабораторной")
            raise Exception("Ошибка при создании таблицы для лабораторной")
        cursor.close()

        db_conn = self.get_lab_conn(database_name)
        db_conn.autocommit = True
        cursor = db_conn.cursor()

        try:
            cursor.execute(structure_sql)
            cursor.execute(data_sql)
            self.commit()
        except Exception:
            logger.error(
                f"[ {uuid} ]: Ошибка при заполнении таблицы данными")
            raise Exception("Ошибка при заполнении таблицы данными")

        cursor.close()
        logger.info(
            f"[ {uuid} ]: В Postgres созданы таблицы и заполнены данными")
        db_conn.close()

    def drop_database(self, uuid) -> bool:
        """
        Метод удаляет таблицу лабораторной из БД
        """
        database_name = uuid.replace("-", "_")

        conn = self.get_conn()
        conn.autocommit = True
        cursor = conn.cursor()

        db_create_query_drop = f"""
                                DROP DATABASE IF EXISTS "{database_name}";
                                """

        try:
            cursor.execute(db_create_query_drop)
            self.commit()
        except Exception:
            logger.error(
                f"[ {uuid} ]: Ошибка при удалении таблицы для лабораторной")
            return False

        logger.info(f"[ {uuid} ]: Таблица в Postgres удалена")
        cursor.close()
        conn.close()
        return True
