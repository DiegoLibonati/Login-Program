from typing import Any

from werkzeug.security import check_password_hash, generate_password_hash

from src.data_access.user_dao import UserDAO


class AuthService:
    def __init__(self, user_dao: UserDAO):
        self._user_dao = user_dao

    def login(self, username: str, password: str) -> tuple[dict[str, Any] | None, str]:
        user = self._user_dao.find_by_username(username)
        if not user:
            return None, "The entered username does not exist in our database."
        if not check_password_hash(user["password"], password):
            return None, "The password does not match the user entered."
        return user, ""

    def register(
        self, username: str, password: str, confirm_password: str
    ) -> tuple[bool, str]:
        if (
            not username
            or not password
            or not confirm_password
            or username.isspace()
            or password.isspace()
        ):
            return False, "You must enter valid fields."

        if password != confirm_password:
            return False, "The passwords entered do not match."

        if self._user_dao.find_by_username(username):
            return False, "The username already exists."

        user = {"username": username, "password": generate_password_hash(password)}
        self._user_dao.insert_user(user)
        return True, "The user was successfully created."
