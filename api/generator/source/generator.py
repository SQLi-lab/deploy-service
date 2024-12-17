from api.generator.source.database_generator import DatabaseGenerator
from api.generator.source.data_generator import DataGenerator


def main_generation(config):
    # Генерация структуры БД
    database_generator = DatabaseGenerator(config)

    # Генерация данных для БД
    data_generator = DataGenerator(database_generator.config, database_generator.tables,
                                   database_generator.extra_table_with_secret)

    return database_generator.database_structure_sql, data_generator.database_data_sql
