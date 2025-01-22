import json

from api.generator.source.utils.paths import (OUTPUT_SQL_DATABASE,
                                              OUTPUT_JSON_DATABASE,
                                              CLOTHES_SHOP_TEMPLATE,
                                              PHARMACY_TEMPLATE,
                                              CAR_SHOP_TEMPLATE, FORUM_TEMPLATE,
                                              CIGAR_SHOP_TEMPLATE,
                                              BET_SITE_TEMPLATE,
                                              PRODUCTS_DELIVERY_TEMPLATE,
                                              MARVEL_TEMPLATE,
                                              BOOK_SHOP_TEMPLATE, ROOT_DIR)
from api.generator.source.utils.file_utils import read_json, write_file, write_json
import random


class DatabaseGenerator:
    def __init__(self, config):
        # Инициализация конфигурации
        self.config = config
        self.validate_config()
        self.target_area = self.init_target_area()
        self.tables = read_json(file_path=self.target_area)

        # Генерация структуры БД
        self.filter_tables()
        self.extra_table_with_secret = self.select_table_with_secret()
        self.database_structure_sql = self.generate_sql()
        # write_file(file_path=OUTPUT_SQL_DATABASE, content=self.database_structure_sql)
        # write_json(file_path=OUTPUT_JSON_DATABASE, data=self.tables)

    def init_target_area(self):
        """ Инициализация предметной области для генерации структуры БД """
        if self.config['target_area'] == 'clotheshop':
            return CLOTHES_SHOP_TEMPLATE
        elif self.config['target_area'] == 'pharmacy':
            return PHARMACY_TEMPLATE
        elif self.config['target_area'] == 'carshop':
            return CAR_SHOP_TEMPLATE
        elif self.config['target_area'] == 'forum':
            return FORUM_TEMPLATE
        elif self.config['target_area'] == 'cigarshop':
            return CIGAR_SHOP_TEMPLATE
        elif self.config['target_area'] == 'bet_site':
            return BET_SITE_TEMPLATE
        elif self.config['target_area'] == 'delivery':
            return PRODUCTS_DELIVERY_TEMPLATE
        elif self.config['target_area'] == 'marvel':
            return MARVEL_TEMPLATE
        elif self.config['target_area'] == 'book_shop':
            return BOOK_SHOP_TEMPLATE
        else:
            return CLOTHES_SHOP_TEMPLATE

    def validate_config(self):
        """ Проверка и исправление конфигурационного файла """

        valid_languages = ["en", "de", "cz", "ru", "fr", "it"]
        valid_sizes = [10, 100, 1000]

        default_values = {
            'target_area': 'default',
            'uuid': '00000000-0000-0000-0000-000000000000',
            'secrets': [],
            'number_extra_tables': random.randint(5, 10),
            'noise_flag': random.choice([True, False]),
            'anonym_flag': random.choice([True, False]),
            'primary_key_flag': random.choice([True, False]),
            'connectivity_degree': random.randint(0, 3),
            'target_language': random.choice(valid_languages),
            'database_size': random.choice(valid_sizes)
        }

        # Проверка отсутствующих ключей
        for key, default in default_values.items():
            if key not in self.config:
                self.config[key] = default

        # Проверка логики значений
        if not (5 <= self.config['number_extra_tables'] <= 10):
            self.config['number_extra_tables'] = random.randint(5, 10)

        if not self.config['primary_key_flag']:
            self.config['connectivity_degree'] = 0

        if self.config['target_language'] not in valid_languages:
            self.config['target_language'] = random.choice(valid_languages)

        if self.config['database_size'] not in valid_sizes:
            self.config['database_size'] = random.choice(valid_sizes)

        if self.config['noise_flag'] and self.config['anonym_flag']:
            if random.choice([True, False]):
                self.config['noise_flag'] = False
            else:
                self.config['anonym_flag'] = False

        # Печать итоговой конфигурации в удобочитаемом формате
        print("[INFO]: Итоговый конфиг:")
        print(json.dumps(self.config, indent=4, ensure_ascii=False))

        return self.config

    def filter_tables(self):
        """ Фильтрация и выборка таблиц """
        mandatory_tables = self.tables["tables"][:5]
        extra_tables = self.tables["tables"][5:]
        
        selected_extra_tables = random.sample(extra_tables, min(self.config['number_extra_tables'], len(extra_tables)))
        selected_tables = mandatory_tables + selected_extra_tables
        self.tables["tables"] = selected_tables

        for table in self.tables["tables"]:
            self.process_foreign_keys(table)

    def select_table_with_secret(self):
        """ Изменяет значение `secret` на `true` в случайной таблице, где `secret` изначально равно `false` """
        tables_with_secret_false = [table for table in self.tables["tables"] if table.get("secret") is False]
        if not tables_with_secret_false:
            print("[Error]: Ошибка конфигурации ключа 'secret' в таблицах - отсутствует 'false' значение")
            return

        random_table = random.choice(tables_with_secret_false)
        random_table["secret"] = True

        tables_with_secret_true = [table["name"] for table in self.tables["tables"] if table.get("secret") is True]
        # print(f"[INFO]: Секретное значение будет добавлено в следующие таблицы: {tables_with_secret_true} \n")
        return random_table["name"]

    def process_foreign_keys(self, table):
        """ Обработка внешних ключей """
        if "foreign_keys" not in table:
            return
        
        table["foreign_keys"] = [
            fk for fk in table["foreign_keys"]
            if fk["references_table"] == table["name"] or fk["references_table"] in [t["name"]
                                                                                     for t in self.tables["tables"]]
        ]

        while self.config['connectivity_degree'] < table.get("connectivity_degree", 0):
            if table["foreign_keys"]:
                table["foreign_keys"].pop()

            if table["connectivity_degree"] == 3:
                table["connectivity_degree"] = 2
            elif table["connectivity_degree"] == 2:
                table["connectivity_degree"] = 0
            elif table["connectivity_degree"] == 1:
                table["connectivity_degree"] = 0

    def create_table(self, table):
        """ Формирует общую SQL-структуру таблицы """
        columns = self.get_columns_definition(table)
        primary_key_sql = self.get_primary_key_sql(table)
        foreign_keys_sql = self.get_foreign_keys_sql(table)

        columns_sql = ",\n".join(columns + primary_key_sql + foreign_keys_sql)
        return f"DROP TABLE IF EXISTS {table['name']} CASCADE;\nCREATE TABLE {table['name']} (\n{columns_sql}\n);"

    def get_columns_definition(self, table):
        """ Формирует набор атрибутов таблицы """
        columns = []
        for col in table["columns"]:
            column_definition = f"    {col['name']} {col['type']}"
            if "constraint" in col and not self.config['noise_flag']:
                column_definition += f" {col['constraint']}"
            columns.append(column_definition)
        return columns

    def get_primary_key_sql(self, table):
        """ Формирует PRIMARY KEY таблицы """
        if self.config['primary_key_flag'] and "primary_key" in table:
            primary_key = table["primary_key"]
            if isinstance(primary_key, list):
                primary_key = ", ".join(primary_key)
            return [f"    PRIMARY KEY ({primary_key})"]
        return []

    @staticmethod
    def get_foreign_keys_sql(table):
        """ Формирует FOREIGN KEYs таблицы """
        foreign_keys = []
        for fk in table.get("foreign_keys", []):
            fk_sql = f"    FOREIGN KEY ({fk['column']}) REFERENCES {fk['references_table']}({fk['references_column']})"
            foreign_keys.append(fk_sql)
        return foreign_keys

    def generate_sql(self):
        """ Формирует общую SQL-структуру БД """
        tables_sql = [self.create_table(table) for table in self.tables["tables"]]
        protection_part_sql = self.get_protection_sql()
        return "\n\n".join(tables_sql) + "\n\n" + protection_part_sql

    @staticmethod
    def get_protection_sql():
        """ Генерирует SQL для ограничения прав доступа к системным таблицам """
        sql = (
            "-- Protection from schema reading\n"
            "REVOKE ALL ON SCHEMA public FROM public;\n"
            "REVOKE SELECT ON ALL TABLES IN SCHEMA information_schema FROM public;\n"
            "REVOKE SELECT ON ALL TABLES IN SCHEMA pg_catalog FROM public;\n"
            "GRANT USAGE ON SCHEMA public TO public;\n"
        )
        return sql

    def create_database(self):
        """ Генерирует SQL-запрос для создания новой базы данных на основе schema_uuid """
        database_name = f'"{self.config['uuid']}"'.replace("-", "_")
        create_db_sql = f'CREATE DATABASE {database_name};\n'
        drop_db_sql = f'DROP DATABASE IF EXISTS {database_name};\n'
        connect_db_command = f'\n\\c {database_name}'
        return drop_db_sql + create_db_sql + connect_db_command
