from api.generator.source.faker_funcs import MyFakerGenerator
import random


"""
SELECT * FROM users;
SELECT * FROM user_personal_info;
SELECT * FROM categories;
SELECT * FROM threads;
SELECT * FROM posts;
SELECT * FROM comments;
SELECT * FROM favorite_posts;
SELECT * FROM banned_users;
SELECT * FROM user_achievements;
SELECT * FROM polls;

"""


class Forum:
    def __init__(self, config):
        self.config = config
        self.fake = MyFakerGenerator(self.config)
        self.admin_login = ''
        self.table_generators = {
            'users': self.generate_user,
            'user_personal_info': self.generate_user_personal_info,
            'categories': self.generate_category,
            'threads': self.generate_thread,
            'posts': self.generate_post,
            'comments': self.generate_comment,
            'favorite_posts': self.generate_favorite_posts,
            'banned_users': self.generate_banned_users,
            'user_achievements': self.generate_user_achievements,
            'polls': self.generate_polls
        }

    def unique_area_modification(self, table_name, records, selected_table):
        """ Добавление ключа CTF для уникальности """
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

        elif table_name == "threads":
            explicit_threads = [record for record in records if not record.get("non_explicit")]
            if explicit_threads:
                thread_to_modify = random.choice(explicit_threads)
                thread_to_modify["secret"] = self.config["secrets"][1]

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

    def generate_category(self, secret="NULL"):
        return {
            "category_name": self.fake.faker_higher_categories('categories_forum'),
            "description": self.fake.faker_text(),
            "secret": secret
        }

    def generate_thread(self, secret="NULL"):
        return {
            "thread_id": self.fake.faker_id(),
            "title": self.fake.faker_categories_forum(),
            "category_name": self.fake.faker_higher_categories('categories_forum'),
            "created_by": self.fake.faker_email(),
            "created_date": self.fake.faker_date_time_this_year(),
            "non_explicit": self.fake.faker_bool(),
            "secret": secret
        }

    def generate_post(self, secret="NULL"):
        return {
            "post_id": self.fake.faker_id(),
            "thread_id": self.fake.faker_id(),
            "author": self.fake.faker_email(),
            "content": self.fake.faker_text(),
            "created_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_comment(self, secret="NULL"):
        return {
            "comment_id": self.fake.faker_id(),
            "post_id": self.fake.faker_id(),
            "author": self.fake.faker_email(),
            "content": self.fake.faker_text(),
            "created_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_favorite_posts(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "post_id": self.fake.faker_id(),
            "added_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_banned_users(self, secret="NULL"):
        return {
            "login": self.fake.faker_email(),
            "ban_reason": self.fake.faker_hashtags('ban_reasons'),
            "banned_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_user_achievements(self, secret="NULL"):
        return {
            "achievement_id": self.fake.faker_id(),
            "login": self.fake.faker_email(),
            "achievement_name": self.fake.faker_phrase('forum_achievements'),
            "description": self.fake.faker_text(),
            "earned_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }

    def generate_polls(self, secret="NULL"):
        return {
            "poll_id": self.fake.faker_id(),
            "thread_id": self.fake.faker_id(),
            "question": self.fake.faker_question(),
            "created_by": self.fake.faker_email(),
            "created_date": self.fake.faker_date_time_this_year(),
            "secret": secret
        }
