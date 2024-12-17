import random
import string

from faker import Faker


class NoiseFunctions:
    def __init__(self, data, language):
        self.fake = Faker(language)
        self.language = language
        self.data = data

    def faker_user_name(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            self.fake.name(),
            "NULL"
        ])

    @staticmethod
    def faker_passport():
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            "NULL"
        ])

    @staticmethod
    def faker_price():
        return random.choice([
            round(random.uniform(-5000, -10), 2),
            "NULL"
        ])

    @staticmethod
    def faker_stock():
        return random.choice([
            random.randint(-1000, -10),
            "NULL"
        ])

    def faker_birthday(self):
        return random.choice([
            self.fake.date_of_birth(minimum_age=400, maximum_age=800),
            "NULL"
        ])

    def faker_date_time_this_year(self):
        return random.choice([
            self.fake.date_of_birth(minimum_age=400, maximum_age=800),
            "NULL"
        ])

    def faker_date_this_year(self):
        return random.choice([
            self.fake.date_of_birth(minimum_age=400, maximum_age=800),
            "NULL"
        ])

    @staticmethod
    def faker_phone_number():
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            "NULL"
        ])

    def faker_order_status(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['order_status'][self.language]),
            "NULL"
        ])

    def faker_text(self):
        return random.choice([
            self.fake.text(ext_word_list=['abc', 'def', 'ghi', 'jkl'], max_nb_chars=30).replace("\n", ""),
            self.fake.text(max_nb_chars=150).replace("\n", ""),
            "NULL"
        ])

    def faker_country(self):
        return random.choice([
            f"Invalid Land {random.randint(1, 9)}",
            self.fake.country(),
            "NULL"
        ])

    def faker_city(self):
        return random.choice([
            f"Bad Value City {random.choice(['Unknown', 'X', 'N/A'])}",
            self.fake.city(),
            "NULL"
        ])

    def faker_full_address(self):
        return random.choice([
            f"Unknown Street {random.randint(0, 999)}, Fake town, {random.choice(['VV', 'ZZ', 'SVO'])}",
            self.fake.address().replace("\n", ", "),
            "NULL"
        ])

    def faker_street_address(self):
        return random.choice([
            f"Unknown Street {random.randint(0, 999)}",
            self.fake.street_address(),
            "NULL"
        ])

    def faker_postcode(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            self.fake.postcode(),
            "NULL"
        ])

    def faker_payment_method(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['payment_methods'][self.language]),
            "NULL"
        ])

    def faker_payment_status(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['payment_status'][self.language]),
            "NULL"
        ])

    @staticmethod
    def faker_higher_categories(area):
        return f"Invalid Higher Category {random.randint(1, 9)}"

    @staticmethod
    def faker_categories(area):
        return f"Invalid Category {random.randint(1, 9)}"

    def faker_items(self, area):
        higher_category = random.choice(list(self.data[area][self.language].keys()))
        category = random.choice(list(self.data[area][self.language][higher_category].keys()))
        return random.choice([
            f"Invalid Item {random.randint(1, 9)}",
            random.choice(list(self.data[area][self.language][higher_category][category]))
        ])

    def faker_hashtags(self, area):
        return random.choice([
            " ".join([f"#{word}" for word in self.fake.words(ext_word_list=['abc', 'def', 'ghi', 'jkl'])]),
            " ".join([f"#{word}" for word in random.sample(self.data[area][self.language], 3)]),
            "NULL"
        ])

    def faker_company_name(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(list(self.data["company_names"][self.language]))
        ])

    def faker_auto_brand(self):
        auto_brand = random.choice(list(self.data["auto_brands"].keys()))
        noise_auto_brand = ''.join(
            random.choice(string.ascii_letters) if random.random() < 0.1 else char
            for char in auto_brand
        )
        return random.choice([
            f"Invalid Brand {random.randint(1, 9)}",
            noise_auto_brand
        ])

    def faker_auto_model(self):
        auto_brand = random.choice(list(self.data["auto_brands"].keys()))
        auto_model = random.choice(list(self.data["auto_brands"][auto_brand]))
        noise_auto_model = ''.join(
            random.choice(string.ascii_letters) if random.random() < 0.1 else char
            for char in auto_model
        )
        return random.choice([
            f"Invalid Model {random.randint(1, 9)}",
            noise_auto_model,
            "NULL"
        ])

    def faker_phrase(self, area):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(list(self.data[area][self.language])),
            "NULL"
        ])

    def faker_question(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            self.fake.sentence(nb_words=5).replace(".", "?"),
            "NULL"
        ])

    def faker_year(self):
        return random.choice([
            int(self.fake.year()) - random.randint(1000, 3000),
            "NULL"
        ])
    
    @staticmethod
    def faker_categories_forum():
        return f"Invalid Category {random.randint(1, 9)}"

    @staticmethod
    def faker_length_cigar():
        return random.choice([
            round(random.uniform(-100, 100), 2),
            "NULL"
        ])

    @staticmethod
    def faker_ring_gauge_cigar():
        return random.choice([
            round(random.uniform(-100, 100), 2),
            "NULL"
        ])

    @staticmethod
    def faker_categories_cigar_shop():
        return f"Invalid Category {random.randint(1, 9)}"

    @staticmethod
    def faker_cigars():
        return f"Invalid Item {random.randint(1, 9)}"

    @staticmethod
    def faker_balance():
        return random.choice([
            round(random.uniform(-10000, 0), 2),
            "NULL"
        ])

    @staticmethod
    def faker_odds():
        return random.choice([
            round(random.uniform(-100, 0), 2),
            "NULL"
        ])

    def faker_bet_outcome_type(self):
        return random.choice([
            f"Invalid Outcome Type {random.randint(1, 9)}",
            random.choice(list(self.data['bet_outcome_type'][self.language])),
            "NULL"
        ])

    def faker_team(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(list(self.data['team_names'][self.language]))
        ])

    @staticmethod
    def faker_categories_sport():
        return f"Invalid Category {random.randint(1, 9)}"

    def faker_categories_products(self):
        return random.choice([
            f"Invalid Category {random.randint(1, 9)}",
            random.choice(list(self.data['categories_products'][self.language].keys())),
            "NULL"
        ])

    def faker_products_name(self):
        category = random.choice(list(self.data['categories_products'][self.language].keys()))
        return random.choice([
            f"Invalid Product Name {random.randint(1, 9)}",
            random.choice(list(self.data['categories_products'][self.language][category])),
            "NULL"
        ])

    def faker_product_shop(self):
        return random.choice([
            f"Invalid Store Name {random.randint(1, 9)}",
            random.choice(list(self.data['product_shop'][self.language])),
            "NULL"
        ])

    def faker_marvel_universe(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            f"{random.choice(self.data['universe_marvel'][self.language])}-{random.randint(1, 1000000)}",
            "NULL"
        ])

    def faker_movie_marvel(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['movie_marvel'][self.language]),
        ])

    def faker_character_marvel(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['characters_marvel'][self.language])
        ])

    def faker_actor_name(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['actors'][self.language]),
            "NULL"
        ])

    def faker_comics_marvel(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            f"{self.fake.word()} {random.choice(self.data['characters_marvel'][self.language])}",
            "NULL"
        ])

    def faker_title_marvel_event(self):
        return random.choice([
            f"EMPTY_STRING#ERROR_CODE#{random.randint(1, 9)}",
            random.choice(self.data['events_marvel'][self.language]),
            "NULL"
        ])

    def faker_genre(self):
        return random.choice([
            f"Invalid Genre {random.randint(1, 9)}",
            random.choice(self.data['genres'][self.language])
        ])

    def faker_book_name(self):
        return random.choice([
            f"Invalid Genre {random.randint(1, 9)}",
            random.choice(self.data['books'][self.language]),
            "NULL"
        ])
