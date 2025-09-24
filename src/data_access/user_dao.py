from typing import Optional

from pymongo import MongoClient


class UserDAO:
    def __init__(self, db: MongoClient):
        self._db = db

    def find_by_username(self, username: str) -> Optional[dict]:
        return self._db.users.find_one({"username": username})

    def insert_user(self, user: dict) -> None:
        self._db.users.insert_one(user)
