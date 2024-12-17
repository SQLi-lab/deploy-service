import random
import re
from datetime import datetime

from faker import Faker


class AnonymFunctions:
    def __init__(self, data, language):
        self.fake = Faker(language)
        self.language = language
        self.data = data

    def faker_user_name(self):
        name = self.fake.name().split()
        return f"{name[0][0]}. {name[1][:3]}***"

    def faker_passport(self):
        passport = self.fake.bothify(self.data['passport_templates'][self.language])
        return passport[:-4] + "****"

    @staticmethod
    def faker_price():
        return round(random.uniform(10, 1000), -1)

    @staticmethod
    def faker_stock():
        return round(random.randint(5, 100), -1)

    def faker_phone_number(self):
        phone = self.fake.phone_number()
        return phone[:2] + '*' * max(0, len(phone) - 4) + phone[-2:] if len(phone) > 4 else phone

    def faker_birthday(self):
        birthday = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        return datetime.strptime(f"{birthday.year}-01-01", "%Y-%m-%d").date()

    def faker_date_time_this_year(self):
        date_time_this_year = self.fake.date_time_this_year().strftime("%Y-%m-01T00:00:00")
        return datetime.strptime(date_time_this_year, "%Y-%m-%dT%H:%M:%S")

    def faker_date_this_year(self):
        date_this_year = self.fake.date_of_birth(minimum_age=18, maximum_age=80)
        return datetime.strptime(f"{date_this_year.year}-01-01", "%Y-%m-%d").date()

    @staticmethod
    def faker_order_status():
        return f"Order Status {random.randint(1, 9)}"

    def faker_text(self):
        return " ".join(self.fake.text(max_nb_chars=150).split()[:10]) + "..."

    def faker_full_address(self):
        address = self.fake.address().replace("\n", ", ")
        address_with_stars = re.sub(r'\d', '*', address)
        parts = address_with_stars.split(", ", 2)
        return f"{parts[0]}, {parts[1]}, ****" if len(parts) > 2 else address_with_stars

    def faker_street_address(self):
        street_address = self.fake.street_address()
        street_address_with_stars = re.sub(r'\d', '*', street_address)
        parts = street_address_with_stars.split(", ", 1)
        return f"{parts[0]}, ****" if len(parts) > 1 else street_address_with_stars

    def faker_postcode(self):
        return self.fake.postcode()[:-4] + "****"

    @staticmethod
    def faker_payment_method():
        return f"Payment Method {random.randint(1, 9)}"

    @staticmethod
    def faker_payment_status():
        return f"Payment Status {random.randint(1, 9)}"

    def faker_year(self):
        return round(int(self.fake.year()), -1)

    @staticmethod
    def faker_balance():
        return round(random.uniform(0, 1000000), -3)
