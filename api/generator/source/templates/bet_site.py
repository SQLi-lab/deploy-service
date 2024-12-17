from api.generator.source.faker_funcs import MyFakerGenerator
import random
from datetime import datetime, timedelta


"""
SELECT * FROM users;
SELECT * FROM user_personal_info;
SELECT * FROM sports_categories;
SELECT * FROM matches;
SELECT * FROM bet_outcomes;
SELECT * FROM user_bets;
SELECT * FROM match_results;
SELECT * FROM bet_statistics;
SELECT * FROM payments;
SELECT * FROM bet_results;

"""


class BetSite:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'sports_categories': self.generate_sports_category,
            'matches': self.generate_match,
            'bet_outcomes': self.generate_bet_outcome,
            'user_bets': self.generate_user_bet,
            'match_results': self.generate_match_result,
            'bet_statistics': self.generate_bet_statistics,
            'payments': self.generate_payment,
            'bet_results': self.generate_bet_result
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
            admin_info = {
                "login": self.admin_login,
                "name": self.fake.faker_user_name(),
                "birth_date": self.fake.faker_birthday(),
                "address": self.fake.faker_full_address(),
                "phone_number": self.fake.faker_phone_number(),
                "balance": self.fake.faker_balance(),
                "secret": self.config["secrets"][0]
            }
            records.append(admin_info)

        elif table_name == "matches":
            current_date = datetime.now().date()
            future_records = [
                record for record in records
                if "match_date" in record
                   and record["match_date"] != "NULL"
                   and record["match_date"] > current_date
            ]
            if not future_records:
                record_to_modify = random.choice(records)
                record_to_modify["match_date"] = (current_date + timedelta(days=7))
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
            "birth_date": self.fake.faker_birthday(),
            "address": self.fake.faker_full_address(),
            "phone_number": self.fake.faker_phone_number(),
            "balance": self.fake.faker_balance(),
            "secret": secret
        }

    def generate_sports_category(self, secret="NULL"):
        return {
            "category": self.fake.faker_categories_sport(),
            "description": self.fake.faker_text(),
            "secret": secret
        }

    def generate_match(self, secret="NULL"):
        return {
            "match_id": self.fake.faker_id(),
            "category": self.fake.faker_categories_sport(),
            "team_first": self.fake.faker_team(),
            "team_second": self.fake.faker_team(),
            "match_date": self.fake.faker_date_this_year(),
            "secret": secret
        }

    def generate_bet_outcome(self, secret="NULL"):
        return {
            "outcome_id": self.fake.faker_id(),
            "match_id": self.fake.faker_id(),
            "outcome_type": self.fake.faker_bet_outcome_type(),
            "description": self.fake.faker_text(),
            "odds_team_first": self.fake.faker_odds(),
            "odds_team_second": self.fake.faker_odds(),
            "secret": secret
        }

    def generate_user_bet(self, secret="NULL"):
        return {
            "bet_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "outcome_id": self.fake.faker_id(),
            "amount": self.fake.faker_price(),
            "bet_date": self.fake.faker_date_this_year(),
            "payout": self.fake.faker_balance(),
            "secret": secret
        }

    def generate_match_result(self, secret="NULL"):
        return {
            "match_id": self.fake.faker_id(),
            "score_team_first": self.fake.faker_rate(),
            "score_team_second": self.fake.faker_rate(),
            "result_time": self.fake.faker_date_this_year(),
            "secret": secret
        }

    def generate_bet_statistics(self, secret="NULL"):
        return {
            "stat_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "bets_placed": self.fake.faker_stock(),
            "bets_won": self.fake.faker_stock(),
            "total_amount_bet": self.fake.faker_price(),
            "total_winnings": self.fake.faker_price(),
            "secret": secret
        }

    def generate_payment(self, secret="NULL"):
        return {
            "payment_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "amount": self.fake.faker_price(),
            "payment_method": self.fake.faker_payment_method(),
            "payment_date": self.fake.faker_date_time_this_year(),
            "payment_status": self.fake.faker_payment_status(),
            "secret": secret
        }

    def generate_bet_result(self, secret="NULL"):
        return {
            "outcome_id": self.fake.faker_id(),
            "match_id": self.fake.faker_id(),
            "is_successful": self.fake.faker_bool(),
            "settlement_time": self.fake.faker_date_time_this_year(),
            "secret": secret
        }
