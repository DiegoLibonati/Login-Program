from test.constants import USERNAME_MOCK
from typing import Any

from pymongo.database import Database

from src.data_access.user_dao import UserDAO


def test_insert_and_find_user(mongo_db: Database) -> None:
    user_dao: UserDAO = UserDAO(mongo_db)
    user: dict[str, Any] = {"username": USERNAME_MOCK, "password": "hashed_pwd"}

    user_dao.insert_user(user)
    found: dict[str, Any] | None = user_dao.find_by_username(USERNAME_MOCK)

    assert found is not None
    assert found["username"] == USERNAME_MOCK
