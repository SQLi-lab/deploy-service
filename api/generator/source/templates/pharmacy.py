from api.generator.source.faker_funcs import MyFakerGenerator
from datetime import datetime, timedelta
import random


"""
SELECT * FROM users;
SELECT * FROM user_personal_info;
SELECT * FROM medication_categories;
SELECT * FROM medications;
SELECT * FROM pharmacies;
SELECT * FROM prescriptions;
SELECT * FROM orders;
SELECT * FROM medication_manufacturers;
SELECT * FROM reviews;
SELECT * FROM pharmacy_medications;

"""


class Pharmacy:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'medication_categories': self.generate_medication_category,
            'medications': self.generate_medication,
            'pharmacies': self.generate_pharmacy,
            'prescriptions': self.generate_prescription,
            'orders': self.generate_order,
            'medication_manufacturers': self.generate_medication_manufacturer,
            'reviews': self.generate_review,
            'pharmacy_medications': self.generate_pharmacy_medication
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

        elif table_name == "medications":
            current_date = datetime.now().date()
            future_records = [
                record for record in records
                if "delivery_date" in record
                   and record["delivery_date"] != "NULL"
                   and record["delivery_date"] > current_date
            ]
            if not future_records:
                record_to_modify = random.choice(records)
                record_to_modify["delivery_date"] = (current_date + timedelta(days=7))
                record_to_modify["secret"] = self.config["secrets"][1]
            else:
                record_to_modify = random.choice(future_records)
                record_to_modify["secret"] = self.config["secrets"][1]

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

    def generate_medication_category(self, secret="NULL"):
        return {
            "category": self.fake.faker_categories("categories_pharmacy"),
            "higher_category": self.fake.faker_higher_categories("categories_pharmacy"),
            "secret": secret
        }

    def generate_medication(self, secret="NULL"):
        return {
            "medication_id": self.fake.faker_id(),
            "name": self.fake.faker_items("categories_pharmacy"),
            "category":  self.fake.faker_categories("categories_pharmacy"),
            "price": self.fake.faker_price(),
            "stock": self.fake.faker_stock(),
            "requires_prescription": self.fake.faker_bool(),
            "delivery_date": self.fake.faker_date_this_year(),
            "secret": secret
        }

    def generate_pharmacy(self, secret="NULL"):
        return {
            "pharmacy_id": self.fake.faker_id(),
            "address": self.fake.faker_full_address(),
            "contact_number": self.fake.faker_phone_number(),
            "secret": secret
        }

    def generate_prescription(self, secret="NULL"):
        return {
            "prescription_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "doctor_name": self.fake.faker_user_name(),
            "issue_date": self.fake.faker_date_this_year(),
            "expiration_date": self.fake.faker_date_this_year(),
            "medication_id": self.fake.faker_id(),
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

    def generate_medication_manufacturer(self, secret="NULL"):
        return {
            "manufacturer_name": self.fake.faker_company_name(),
            "country": self.fake.faker_country(),
            "contact_number": self.fake.faker_phone_number(),
            "contact_email": self.fake.faker_email(),
            "secret": secret
        }

    def generate_review(self, secret="NULL"):
        return {
            "review_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "medication_id": self.fake.faker_id(),
            "rating": self.fake.faker_rate(),
            "review_text": self.fake.faker_text(),
            "review_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_pharmacy_medication(self, secret="NULL"):
        return {
            "pharmacy_id": self.fake.faker_id(),
            "medication_id": self.fake.faker_id(),
            "price": self.fake.faker_price(),
            "stock": self.fake.faker_stock(),
            "secret": secret
        }
