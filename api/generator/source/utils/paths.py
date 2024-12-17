from pathlib import Path

# Корень проекта
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Конфигурация
CONFIG_FILE = ROOT_DIR / "config" / "config.json"

# Данные
DATA_DIR = ROOT_DIR / "data"
INPUT_DATA = DATA_DIR / "data.json"

RESULTS_SQL_DIR = DATA_DIR / "results_sql"
OUTPUT_SQL_DATABASE = RESULTS_SQL_DIR / "output_database_structure.sql"
OUTPUT_SQL_DATA = RESULTS_SQL_DIR / "output_data.sql"

RESULTS_JSON_DIR = DATA_DIR / "results_json"
OUTPUT_JSON_DATABASE = RESULTS_JSON_DIR / "output_database_structure.json"
OUTPUT_JSON_DATA = RESULTS_JSON_DIR / "output_data.json"

# Шаблоны
TEMPLATES_DIR = ROOT_DIR / "templates"
CLOTHES_SHOP_TEMPLATE = TEMPLATES_DIR / "clothes_shop.json"
PHARMACY_TEMPLATE = TEMPLATES_DIR / "pharmacy.json"
CAR_SHOP_TEMPLATE = TEMPLATES_DIR / "car_shop.json"
FORUM_TEMPLATE = TEMPLATES_DIR / "forum.json"
CIGAR_SHOP_TEMPLATE = TEMPLATES_DIR / "cigar_shop.json"
BET_SITE_TEMPLATE = TEMPLATES_DIR / "bet_site.json"
PRODUCTS_DELIVERY_TEMPLATE = TEMPLATES_DIR / "products_delivery.json"
MARVEL_TEMPLATE = TEMPLATES_DIR / "marvel.json"
BOOK_SHOP_TEMPLATE = TEMPLATES_DIR / "book_shop.json"

# Модули
SOURCE_DIR = ROOT_DIR / "source"
SOURCE_TEMPLATES_DIR = SOURCE_DIR / "templates"
