from api.generator.source.faker_funcs import MyFakerGenerator
import random


class Marvel:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'characters': self.generate_character,
            'movies': self.generate_movie,
            'comics': self.generate_comic,
            'movie_cast': self.generate_movie_cast,
            'events': self.generate_event,
            'character_comics': self.generate_character_comic,
            'user_comments': self.generate_user_comment,
            'empty_table': self.generate_empty_table
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

        elif table_name == "characters":
            unreleased_characters = [record for record in records if not record.get("released")]
            if unreleased_characters:
                character_to_modify = random.choice(unreleased_characters)
                character_to_modify["secret"] = self.config["secrets"][1]

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

    def generate_character(self, secret="NULL"):
        return {
            "character_name": self.fake.faker_character_marvel(),
            "description": self.fake.faker_hashtags('character_descriptions'),
            "universe": self.fake.faker_marvel_universe(),
            "power_level": self.fake.faker_stock(),
            "released": self.fake.faker_bool(),
            "secret": secret
        }

    def generate_movie(self, secret="NULL"):
        return {
            "movie_name": self.fake.faker_movie_marvel(),
            "release_date": self.fake.faker_date_this_year(),
            "description": self.fake.faker_text(),
            "director": self.fake.faker_user_name(),
            "secret": secret
        }

    def generate_comic(self, secret="NULL"):
        return {
            "comic_id": self.fake.faker_id(),
            "title": self.fake.faker_comics_marvel(),
            "issue_number": self.fake.faker_id(),
            "release_date": self.fake.faker_date_this_year(),
            "description": self.fake.faker_text(),
            "secret": secret
        }

    def generate_movie_cast(self, secret="NULL"):
        return {
            "movie_name": self.fake.faker_movie_marvel(),
            "character_name": self.fake.faker_character_marvel(),
            "actor_name": self.fake.faker_actor_name(),
            "secret": secret
        }

    def generate_event(self, secret="NULL"):
        return {
            "event_id": self.fake.faker_id(),
            "title": self.fake.faker_title_marvel_event(),
            "description": self.fake.faker_text(),
            "start_date": self.fake.faker_date_this_year(),
            "end_date": self.fake.faker_date_this_year(),
            "secret": secret
        }

    def generate_character_comic(self, secret="NULL"):
        return {
            "comic_id": self.fake.faker_id(),
            "character_name": self.fake.faker_character_marvel(),
            "secret": secret
        }

    def generate_user_comment(self, secret="NULL"):
        return {
            "comment_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "text": self.fake.faker_text(),
            "timestamp": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_empty_table(self, secret="NULL"):
        return {
            "record_id": self.fake.faker_id(),
            "description": "Just Try One More Time",
            "secret": secret
        }
