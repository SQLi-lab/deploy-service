import json
from datetime import date


def read_file(file_path: str, encoding="utf-8") -> str:
    """Чтение содержимого текстового файла."""
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {file_path} не найден.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении файла {file_path}: {e}")


def write_file(file_path: str, content: str, encoding="utf-8") -> None:
    """Запись текста в файл."""
    try:
        with open(file_path, "w", encoding=encoding) as file:
            file.write(content)
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи в файл {file_path}: {e}")


def read_json(file_path: str, encoding="utf-8") -> dict:
    """Чтение данных из JSON файла."""
    try:
        with open(file_path, "r", encoding=encoding) as file:
            return json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"JSON файл {file_path} не найден.")
    except json.JSONDecodeError:
        raise ValueError(f"Файл {file_path} содержит некорректный JSON.")
    except Exception as e:
        raise RuntimeError(f"Ошибка при чтении JSON файла {file_path}: {e}")


def write_json(file_path: str, data: dict) -> None:
    """Запись данных в JSON файл."""
    def default_serializer(obj):
        if isinstance(obj, date):
            return obj.isoformat()  # Преобразование даты в строку в формате YYYY-MM-DD
        raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")

    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False, default=default_serializer)
    except Exception as e:
        raise RuntimeError(f"Ошибка при записи JSON файла {file_path}: {e}")
