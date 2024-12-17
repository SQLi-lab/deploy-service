from api.generator.source.faker_funcs import MyFakerGenerator
import random

"""
SELECT * FROM users;
SELECT * FROM user_personal_info;
SELECT * FROM genres;
SELECT * FROM books;
SELECT * FROM orders;
SELECT * FROM reviews;
SELECT * FROM shipping_addresses;
SELECT * FROM payments;
SELECT * FROM favorite_books;
SELECT * FROM shopping_cart;
"""


class BookShop:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'genres': self.generate_genre,
            'books': self.generate_book,
            'orders': self.generate_order,
            'reviews': self.generate_review,
            'shipping_addresses': self.generate_shipping_address,
            'payments': self.generate_payment,
            'favorite_books': self.generate_favorite_book,
            'shopping_cart': self.generate_shopping_cart,
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
                "birth_date": self.fake.faker_birthday(),
                "address": self.fake.faker_full_address(),
                "phone_number": self.fake.faker_phone_number(),
                "secret": self.config["secrets"][0]
            }
            records.append(admin_user_ctf_info)

        elif table_name == "books":
            unreleased_books = [record for record in records if not record.get("released")]
            if unreleased_books:
                book_to_modify = random.choice(unreleased_books)
                book_to_modify["secret"] = self.config["secrets"][1]

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
            "birth_date": self.fake.faker_birthday(),
            "address": self.fake.faker_full_address(),
            "phone_number": self.fake.faker_phone_number(),
            "secret": secret
        }

    def generate_genre(self, secret="NULL"):
        return {
            "genre_name": self.fake.faker_genre(),
            "description": self.fake.faker_text(),
            "secret": secret
        }

    def generate_book(self, secret="NULL"):
        return {
            "article": self.fake.faker_id(),
            "name": self.fake.faker_book_name(),
            "genre_name": self.fake.faker_genre(),
            "author": self.fake.faker_user_name(),
            "price": self.fake.faker_price(),
            "stock": self.fake.faker_stock(),
            "released": self.fake.faker_bool(),
            "secret": secret
        }

    def generate_order(self, secret="NULL"):
        return {
            "order_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "order_date": self.fake.faker_date_time_this_year(),
            "status": self.fake.faker_order_status(),
            "secret": secret
        }

    def generate_review(self, secret="NULL"):
        return {
            "review_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "article": self.fake.faker_id(),
            "rating": self.fake.faker_rate(),
            "review_text": self.fake.faker_text(),
            "review_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_shipping_address(self, secret="NULL"):
        return {
            "address_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "country": self.fake.faker_country(),
            "city": self.fake.faker_city(),
            "street": self.fake.faker_street_address(),
            "postal_code": self.fake.faker_postcode(),
            "secret": secret
        }

    def generate_payment(self, secret="NULL"):
        return {
            "order_id": self.fake.faker_id(),
            "payment_method": self.fake.faker_payment_method(),
            "amount": self.fake.faker_price(),
            "payment_status": self.fake.faker_payment_status(),
            "secret": secret
        }

    def generate_favorite_book(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "article": self.fake.faker_id(),
            "added_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_shopping_cart(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "article": self.fake.faker_id(),
            "quantity": self.fake.faker_stock(),
            "secret": secret
        }
