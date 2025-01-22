from api.generator.source.templates.clothes_shop import ClothesShop
from api.generator.source.templates.pharmacy import Pharmacy
from api.generator.source.templates.car_shop import CarShop
from api.generator.source.templates.forum import Forum
from api.generator.source.templates.cigar_shop import CigarShop
from api.generator.source.templates.bet_site import BetSite
from api.generator.source.templates.products_delivery import ProductDelivery
from api.generator.source.templates.marvel import Marvel
from api.generator.source.templates.book_shop import BookShop
from api.generator.source.utils.file_utils import write_file, write_json
from api.generator.source.utils.paths import OUTPUT_SQL_DATA, OUTPUT_JSON_DATA
import random
import datetime


class DataGenerator:
    def __init__(self, config, tables, extra_table_with_secret):
        # Инициализация переменных
        self.config = config
        self.tables = tables
        self.extra_table_with_secret = extra_table_with_secret

        # Генерация данных в зависимости от предметной области
        self.database = self.init_target_area()
        self.database_data_sql = self.main_generation()

    def init_target_area(self):
        """ Инициализация предметной области для генерации данных """
        if self.config['target_area'] == 'clotheshop':
            return ClothesShop(self.config)
        elif self.config['target_area'] == 'pharmacy':
            return Pharmacy(self.config)
        elif self.config['target_area'] == 'carshop':
            return CarShop(self.config)
        elif self.config['target_area'] == 'forum':
            return Forum(self.config)
        elif self.config['target_area'] == 'cigarshop':
            return CigarShop(self.config)
        elif self.config['target_area'] == 'bet_site':
            return BetSite(self.config)
        elif self.config['target_area'] == 'delivery':
            return ProductDelivery(self.config)
        elif self.config['target_area'] == 'marvel':
            return Marvel(self.config)
        elif self.config['target_area'] == 'book_shop':
            return BookShop(self.config)
        else:
            return ClothesShop(self.config)

    def main_generation(self):
        """ Основная функция для генерации данных БД """
        # Этап 1: Генерация данных
        generated_data = self.generate_initial_data()

        # Этап 2: Замена внешних ключей
        processed_generated_data = self.replace_foreign_keys(generated_data)

        # Этап 3: Проверка уникальности primary key
        final_data = self.check_primary_key_uniqueness(processed_generated_data)

        # Этап 4: Генерация вывода (INSERT) для БД
        output_sql, output_json = self.generate_sql_output(final_data)

        # Запись данных в форматах sql и json
        # write_file(file_path=OUTPUT_SQL_DATA, content=output_sql)
        # write_json(file_path=OUTPUT_JSON_DATA, data=output_json)

        return output_sql

    def generate_table_data(self, table_name, num_records):
        """ Генерация данных для одной таблицы """
        values = []
        generator = self.database.table_generators.get(table_name)
        if not generator:
            raise ValueError(f"Generator for table '{table_name}' not found.")

        for _ in range(num_records):
            values.append(generator())

        return values

    def generate_initial_data(self):
        """ Генерация данных для всех таблиц """
        generated_data = {}
        for table in self.tables["tables"]:
            table_name = table["name"]
            # print(f"[INFO]: Генерация данных для таблицы {table_name} подождите...")

            # Генерация данных для таблицы
            table_data = self.generate_table_data(table_name, self.config['database_size'])
            generated_data[table_name] = table_data
        print("")

        return generated_data

    def check_primary_key_uniqueness(self, generated_data):
        """ Проверка уникальности записей по значениям Primary Key для всех таблиц """
        processed_data = {}
        for table in self.tables["tables"]:
            table_name = table["name"]
            primary_keys = table.get("primary_key", [])
            table_data = generated_data[table_name]
            if self.config['primary_key_flag']:
                unique_records = set()
                unique_data = []
                for record in table_data:
                    pk_values = tuple(record[pk] for pk in primary_keys) \
                        if isinstance(primary_keys, list) else (record[primary_keys],)
                    if pk_values not in unique_records:
                        unique_records.add(pk_values)
                        unique_data.append(record)
                processed_data[table_name] = unique_data
            else:
                processed_data[table_name] = table_data

        return processed_data

    def replace_foreign_keys(self, generated_data):
        """ Замена внешних ключей на реальные значения из других таблиц """
        for table in self.tables["tables"]:
            table_name = table["name"]
            if "foreign_keys" in table:
                # print(f"[INFO]: Замена внешних ключей для таблицы {table_name} подождите...")
                for record in generated_data[table_name]:
                    for fk in table["foreign_keys"]:
                        ref_table = fk["references_table"]
                        ref_column = fk["references_column"]
                        fk_column = fk["column"]
                        if ref_table in generated_data:
                            referenced_values = {item[ref_column] for item in generated_data[ref_table]}
                            if fk_column == table.get("primary_key", ""):
                                used_values = {item[fk_column] for item in generated_data[table_name]}
                                available_values = referenced_values - used_values
                                if available_values:
                                    record[fk_column] = random.choice(list(available_values))
                            else:
                                record[fk_column] = random.choice(list(referenced_values))
        print("")
        return generated_data

    def generate_sql_output(self, generated_data):
        """ Генерация INSERT записей для сгенерированных данных """
        output_sql = []
        output_json = {}
        for table_name, records in generated_data.items():
            self.database.unique_area_modification(table_name, records, self.extra_table_with_secret)
            output_sql.append("--")
            if records:
                columns = ', '.join(records[0].keys())
                for record in records:
                    values = ', '.join(
                        "{}".format(value) if value == "NULL" else
                        "'{}'".format(value.replace("'", "''")) if isinstance(value, str) else
                        "'{}'".format(value) if isinstance(value, datetime.date) else str(value)
                        for value in record.values()
                    )
                    output_sql.append(f"INSERT INTO {table_name} ({columns}) VALUES ({values});")
            output_sql.append("\n")
            output_json[table_name] = records

        output_sql = "\n".join(output_sql)
        return output_sql, output_json
