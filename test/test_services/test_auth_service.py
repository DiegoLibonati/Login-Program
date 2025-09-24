from test.constants import PASSWORD_MOCK, USERNAME_MOCK

from pymongo.database import Database

from src.data_access.user_dao import UserDAO
from src.services.auth_service import AuthService


def test_register_and_login(mongo_db: Database) -> None:
    user_dao: UserDAO = UserDAO(mongo_db)
    service: AuthService = AuthService(user_dao)

    ok, msg = service.register(USERNAME_MOCK, PASSWORD_MOCK, PASSWORD_MOCK)
    assert ok is True
    assert msg == "The user was successfully created."

    user, msg = service.login(USERNAME_MOCK, PASSWORD_MOCK)
    assert user is not None
    assert msg == ""

    user, msg = service.login(USERNAME_MOCK, PASSWORD_MOCK + "X")
    assert user is None
    assert msg == "The password does not match the user entered."

    user, msg = service.login("ghost", "1234")
    assert user is None
    assert msg == "The entered username does not exist in our database."
