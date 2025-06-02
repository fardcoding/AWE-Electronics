import json
import os

class Account:
    _users = {}

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    @classmethod
    def load_users(cls, filepath="data/users.json"):
        if os.path.exists(filepath):
            with open(filepath, "r") as f:
                data = json.load(f)
                for username, details in data.items():
                    cls._users[username] = Account(username, details["password"], details["email"])

    @classmethod
    def save_users(cls, filepath="data/users.json"):
        data = {
            username: {
                "password": acc.password,
                "email": acc.email
            }
            for username, acc in cls._users.items()
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=4)

    @classmethod
    def register(cls, username, password, email):
        if username in cls._users:
            raise ValueError("Username already exists.")
        if not username or not password or '@' not in email:
            raise ValueError("Invalid registration details.")
        account = Account(username, password, email)
        cls._users[username] = account
        cls.save_users()
        return True

    @classmethod
    def authenticate(cls, username, password):
        user = cls._users.get(username)
        if user and user.password == password:
            return user
        return None
