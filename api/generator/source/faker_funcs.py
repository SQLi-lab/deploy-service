from faker import Faker
from api.generator.source.noise_faker_funcs import NoiseFunctions
from api.generator.source.anonym_faker_funcs import AnonymFunctions
from api.generator.source.utils.paths import INPUT_DATA
from api.generator.source.utils.file_utils import read_json
import random


def modification_decorator(func):
    """Декоратор для модификации данных (шум/анонимизация)"""
    def wrapper(self, *args, **kwargs):
        if self.config['noise_flag']:
            if random.random() <= 0.3:
                noise_language = random.choice(list(self.noise_instances.keys()))
                noise_instance = self.noise_instances[noise_language]
                if hasattr(noise_instance, func.__name__):
                    noise_method = getattr(noise_instance, func.__name__)
                    return noise_method(*args, **kwargs)
                else:
                    return func(self, *args, **kwargs)
        elif self.config['anonym_flag']:
            if hasattr(self.anonym_instance, func.__name__):
                anonym_method = getattr(self.anonym_instance, func.__name__)
                return anonym_method(*args, **kwargs)
            else:
                return func(self, *args, **kwargs)
        return func(self, *args, **kwargs)
    return wrapper


class MyFakerGenerator:
    def __init__(self, config):
        # Инициализация основных переменных
        self.config = config
        self.language = self.config['target_language']
        self.fake = Faker(self.language)
        self.data = read_json(INPUT_DATA)

        # Создаем словарь с экземплярами NoiseFunctions для всех поддерживаемых языков
        self.noise_instances = {
            lang: NoiseFunctions(data=self.data, language=lang)
            for lang in ["en", "de", "cz", "ru", "fr", "it"]
        }

        # Создаем экземпляр AnonymFunctions
        self.anonym_instance = AnonymFunctions(data=self.data, language=self.language)

    def faker_ibks_ctf(self):
        return f"ibks_ctf{{{self.fake.sha256()[:16]}}}"

    @modification_decorator
    def faker_user_name(self):
        return self.fake.name()

    def faker_password(self):
        return self.fake.password(length=16)

    def faker_email(self):
        return f"{Faker().word()}_{Faker().word()}@{self.fake.free_email_domain()}"

    @modification_decorator
    def faker_passport(self):
        return self.fake.bothify(self.data['passport_templates'][self.language])

    @modification_decorator
    def faker_price(self):
        return round(random.uniform(1, 1000), 2)

    @modification_decorator
    def faker_stock(self):
        return random.randint(1, 100)

    @modification_decorator
    def faker_phone_number(self):
        return self.fake.phone_number()

    @modification_decorator
    def faker_birthday(self):
        return self.fake.date_of_birth(minimum_age=18, maximum_age=80)

    @modification_decorator
    def faker_date_time_this_year(self):
        return self.fake.date_time_this_year(before_now=True, after_now=True)

    @modification_decorator
    def faker_date_this_year(self):
        return self.fake.date_this_year(before_today=True, after_today=True)

    def faker_id(self):
        return int(self.fake.unique.ean(length=13))

    def faker_bool(self):
        return self.fake.boolean(chance_of_getting_true=60)

    @modification_decorator
    def faker_order_status(self):
        return random.choice(self.data['order_status'][self.language])

    @staticmethod
    def faker_rate():
        return random.randint(0, 5)

    @modification_decorator
    def faker_text(self):
        return self.fake.text(max_nb_chars=150).replace("\n", "")

    @modification_decorator
    def faker_country(self):
        return self.fake.country()

    @modification_decorator
    def faker_city(self):
        return self.fake.city()

    @modification_decorator
    def faker_full_address(self):
        return self.fake.address().replace("\n", ", ")

    @modification_decorator
    def faker_street_address(self):
        return self.fake.street_address()

    @modification_decorator
    def faker_postcode(self):
        return self.fake.postcode()

    @modification_decorator
    def faker_payment_method(self):
        return random.choice(self.data['payment_methods'][self.language])

    @modification_decorator
    def faker_payment_status(self):
        return random.choice(self.data['payment_status'][self.language])

    @modification_decorator
    def faker_higher_categories(self, area):
        return random.choice(list(self.data[area][self.language].keys()))

    @modification_decorator
    def faker_categories(self, area):
        higher_category = random.choice(list(self.data[area][self.language].keys()))
        return random.choice(list(self.data[area][self.language][higher_category].keys()))

    @modification_decorator
    def faker_items(self, area):
        higher_category = random.choice(list(self.data[area][self.language].keys()))
        category = random.choice(list(self.data[area][self.language][higher_category].keys()))
        return random.choice(list(self.data[area][self.language][higher_category][category]))

    @modification_decorator
    def faker_hashtags(self, area):
        return " ".join([f"#{word}" for word in random.sample(self.data[area][self.language], 3)])

    @modification_decorator
    def faker_company_name(self):
        return random.choice(list(self.data["company_names"][self.language]))

    @modification_decorator
    def faker_auto_brand(self):
        return random.choice(list(self.data["auto_brands"].keys()))

    @modification_decorator
    def faker_auto_model(self):
        auto_brand = random.choice(list(self.data["auto_brands"].keys()))
        return random.choice(list(self.data["auto_brands"][auto_brand]))

    @modification_decorator
    def faker_phrase(self, area):
        return random.choice(list(self.data[area][self.language]))

    @modification_decorator
    def faker_question(self):
        return self.fake.sentence(nb_words=5).replace(".", "?")

    @modification_decorator
    def faker_year(self):
        return int(self.fake.year())

    @modification_decorator
    def faker_categories_forum(self):
        higher_category = random.choice(list(self.data['categories_forum'][self.language].keys()))
        return random.choice(list(self.data['categories_forum'][self.language][higher_category]))

    @modification_decorator
    def faker_length_cigar(self):
        return round(random.uniform(4, 7), 2)

    @modification_decorator
    def faker_ring_gauge_cigar(self):
        return round(random.uniform(42, 64), 2)

    @modification_decorator
    def faker_categories_cigar_shop(self):
        return random.choice(list(self.data['cigars'].keys()))

    @modification_decorator
    def faker_cigars(self):
        cigars_category = random.choice(list(self.data['cigars'].keys()))
        return random.choice(list(self.data['cigars'][cigars_category]))

    @modification_decorator
    def faker_balance(self):
        return round(random.uniform(0, 10000), 2)

    @modification_decorator
    def faker_odds(self):
        return round(random.uniform(0, 50), 2)

    @modification_decorator
    def faker_bet_outcome_type(self):
        return random.choice(list(self.data['bet_outcome_type'][self.language]))

    @modification_decorator
    def faker_team(self):
        return random.choice(list(self.data['team_names'][self.language]))

    @modification_decorator
    def faker_categories_sport(self):
        return random.choice(list(self.data['sports'][self.language]))

    @modification_decorator
    def faker_categories_products(self):
        return random.choice(list(self.data['categories_products'][self.language].keys()))

    @modification_decorator
    def faker_products_name(self):
        category = random.choice(list(self.data['categories_products'][self.language].keys()))
        return random.choice(list(self.data['categories_products'][self.language][category]))

    @modification_decorator
    def faker_product_shop(self):
        return random.choice(list(self.data['product_shop'][self.language]))

    @modification_decorator
    def faker_marvel_universe(self):
        return f"{self.data['universe_marvel'][self.language]}-{random.randint(1, 1000000)}"

    @modification_decorator
    def faker_movie_marvel(self):
        return random.choice(self.data['movie_marvel'][self.language])

    @modification_decorator
    def faker_character_marvel(self):
        return random.choice(self.data['characters_marvel'][self.language])

    @modification_decorator
    def faker_actor_name(self):
        return random.choice(self.data['actors'][self.language])

    @modification_decorator
    def faker_comics_marvel(self):
        return (f"{random.choice(self.data['character_descriptions'][self.language])} "
                f"{random.choice(self.data['characters_marvel'][self.language])}")

    @modification_decorator
    def faker_title_marvel_event(self):
        return random.choice(self.data['events_marvel'][self.language])

    @modification_decorator
    def faker_genre(self):
        return random.choice(self.data['genres'][self.language])

    @modification_decorator
    def faker_book_name(self):
        return random.choice(self.data['books'][self.language])
