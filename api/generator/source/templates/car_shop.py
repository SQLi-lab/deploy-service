from api.generator.source.faker_funcs import MyFakerGenerator
import random

"""
SELECT * FROM users;
SELECT * FROM user_personal_info;
SELECT * FROM car_brand;
SELECT * FROM car_models;
SELECT * FROM car_dealerships;
SELECT * FROM inventory;
SELECT * FROM orders;
SELECT * FROM reviews;
SELECT * FROM favorite_cars;
SELECT * FROM price_history;

"""


class CarShop:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'car_brand': self.generate_car_brand,
            'car_models': self.generate_car_model,
            'car_dealerships': self.generate_car_dealership,
            'inventory': self.generate_inventory,
            'orders': self.generate_order,
            'reviews': self.generate_review,
            'favorite_cars': self.generate_favorite_car,
            'price_history': self.generate_price_history
        }

    def unique_area_modification(self, table_name, records, selected_table):
        """ Функция для добавления к сгенерированным данным ключа CTF """
        if table_name == "users":
            admin_user = {
                "login": self.fake.faker_email(),
                "password": self.fake.faker_password(),
                "role": "admin"
            }
            self.admin_login = admin_user["login"]
            records.append(admin_user)

        elif table_name == "user_personal_info":
            admin_user_ctf_info = {
                "login": self.admin_login,
                "name": self.fake.faker_user_name(),
                "passport_number": self.fake.faker_passport(),
                "birth_date": self.fake.faker_birthday(),
                "address": self.fake.faker_full_address(),
                "phone_number": self.fake.faker_phone_number(),
                "secret": self.config["secrets"][0]
            }
            records.append(admin_user_ctf_info)

        elif table_name == "car_models":
            defective_models = [record for record in records if record.get("defective")]
            if defective_models:
                model_to_modify = random.choice(defective_models)
                model_to_modify["secret"] = self.config["secrets"][1]

        elif table_name == selected_table:
            modification = random.choice(records)
            modification["secret"] = self.config["secrets"][2]

        return records

    def generate_user(self):
        return {
            "login": self.fake.faker_email(),
            "password": self.fake.faker_password(),
            "role": "user"
        }

    def generate_user_personal_info(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "name": self.fake.faker_user_name(),
            "passport_number": self.fake.faker_passport(),
            "birth_date": self.fake.faker_birthday(),
            "address": self.fake.faker_full_address(),
            "phone_number": self.fake.faker_phone_number(),
            "secret": secret
        }

    def generate_car_brand(self, secret="NULL"):
        return {
            "brand": self.fake.faker_auto_brand(),
            "description": self.fake.faker_text(),
            "secret": secret
        }

    def generate_car_model(self, secret="NULL"):
        return {
            "model_id": self.fake.faker_id(),
            "brand": self.fake.faker_auto_brand(),
            "model_name": self.fake.faker_auto_model(),
            "year": self.fake.faker_year(),
            "base_price": self.fake.faker_price(),
            "defective": self.fake.faker_bool(),
            "secret": secret
        }

    def generate_car_dealership(self, secret="NULL"):
        return {
            "dealership_id": self.fake.faker_id(),
            "brand": self.fake.faker_auto_brand(),
            "address": self.fake.faker_full_address(),
            "phone_number": self.fake.faker_phone_number(),
            "email": self.fake.faker_email(),
            "secret": secret
        }

    def generate_inventory(self, secret="NULL"):
        return {
            "vin": self.fake.faker_id(),
            "model_id": self.fake.faker_id(),
            "stock_status": self.fake.faker_bool(),
            "price": self.fake.faker_price(),
            "dealership_id": self.fake.faker_id(),
            "secret": secret
        }

    def generate_order(self, secret="NULL"):
        return {
            "order_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "order_date": self.fake.faker_date_time_this_year(),
            "status": self.fake.faker_order_status(),
            "model_id": self.fake.faker_id(),
            "secret": secret
        }

    def generate_review(self, secret="NULL"):
        return {
            "review_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "model_id": self.fake.faker_id(),
            "rating": self.fake.faker_rate(),
            "review_text": self.fake.faker_text(),
            "review_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_favorite_car(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "model_id": self.fake.faker_id(),
            "added_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_price_history(self, secret="NULL"):
        return {
            "history_id": self.fake.faker_id(),
            "model_id": self.fake.faker_id(),
            "old_price": self.fake.faker_price(),
            "new_price": self.fake.faker_price(),
            "changed_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }
