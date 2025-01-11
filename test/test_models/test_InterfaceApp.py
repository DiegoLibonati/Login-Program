import logging

import pytest
# from unittest.mock import patch
# from unittest.mock import MagicMock

from src.app import load_config
from src.app import load_mongo
from src.models.InterfaceApp import InterfaceApp
from src.utils.constants import PRIMARY_COLOR

from test.constants import USERNAME_MOCK
from test.constants import PASSWORD_MOCK


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root = interface_app._root
    root.update()

    title = root.title()
    geometry = root.geometry().split("+")[0]
    resizable = root.resizable()
    config_bg = root.cget("bg")

    user = interface_app.user
    username = interface_app.username
    config_mongo = interface_app.config_mongo
    db = interface_app.db

    assert title == "Login"
    assert geometry == "400x400"
    assert resizable == (False, False)
    assert config_bg == PRIMARY_COLOR

    assert config_mongo
    assert db is not None
    assert username == "N/A"
    assert not user

def test_create_widgets(interface_app: InterfaceApp) -> None:
    interface_app._create_widgets()

    assert interface_app._text_confirm_login.get() == "Welcome"
    assert interface_app._text_username_login.get() == ""
    assert interface_app._text_password_login.get() == ""

    assert interface_app._label_confirm_login.cget("text") == "Welcome"
    assert interface_app._label_username_login.cget("text") == "Username"
    assert interface_app._label_password_login.cget("text") == "Password"

    assert interface_app._entry_username_login.get() == ""
    assert interface_app._entry_password_login.get() == ""

def test_window_register(interface_app: InterfaceApp) -> None:
    interface_app._window_register()

    title = interface_app._win_register.title()
    resizable = interface_app._win_register.resizable()
    config_bg = interface_app._win_register.cget("bg")

    assert title == "Register"
    assert resizable == (False, False)
    assert config_bg == PRIMARY_COLOR

    assert interface_app._text_confirm_register.get() == ""
    assert interface_app._text_username_register.get() == ""
    assert interface_app._text_password_register.get() == ""
    assert interface_app._text_confirm_password_register.get() == ""

    assert interface_app._label_username_register.cget("text") == "Username"
    assert interface_app._label_password_register.cget("text") == "Password"
    assert interface_app._label_confirm_password_register.cget("text") == "Confirm password"
    
    assert interface_app._entry_username_register.get() == ""
    assert interface_app._entry_password_register.get() == ""
    assert interface_app._entry_confirm_password_register.get() == ""

def test_register_invalid_fields(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_register.insert(0, USERNAME_MOCK)
    interface_app._entry_password_register.insert(0, PASSWORD_MOCK)
    interface_app._entry_confirm_password_register.insert(0, "")

    interface_app._register()

    assert interface_app._text_confirm_register.get() == "You must enter valid fields."

    interface_app._entry_username_register.delete(0, "end")
    interface_app._entry_password_register.delete(0, "end")
    interface_app._entry_confirm_password_register.delete(0, "end")

def test_register_password_dont_match(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_register.insert(0, USERNAME_MOCK)
    interface_app._entry_password_register.insert(0, PASSWORD_MOCK)
    interface_app._entry_confirm_password_register.insert(0, PASSWORD_MOCK + "123")

    interface_app._register()

    assert interface_app._text_confirm_register.get() == "The passwords entered do not match."

    interface_app._entry_username_register.delete(0, "end")
    interface_app._entry_password_register.delete(0, "end")
    interface_app._entry_confirm_password_register.delete(0, "end")

@pytest.mark.usefixtures("mongo_test_db")
def test_register(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_register.insert(0, USERNAME_MOCK)
    interface_app._entry_password_register.insert(0, PASSWORD_MOCK)
    interface_app._entry_confirm_password_register.insert(0, PASSWORD_MOCK)

    interface_app._register()

    assert interface_app._text_confirm_register.get() == "The user was successfully created."

@pytest.mark.usefixtures("mongo_test_db")
def test_login_user_not_exists(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_login.insert(0, USERNAME_MOCK + "not_exist")
    interface_app._entry_password_login.insert(0, PASSWORD_MOCK)

    interface_app._login()

    assert interface_app._text_confirm_login.get() == "The entered username does not exist in our database."

    interface_app._entry_username_login.delete(0, "end")
    interface_app._entry_password_login.delete(0, "end")

@pytest.mark.usefixtures("mongo_test_db")
def test_login_password_dont_match(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_login.insert(0, USERNAME_MOCK)
    interface_app._entry_password_login.insert(0, PASSWORD_MOCK + "123")

    interface_app._login()

    assert interface_app._text_confirm_login.get() == "The password does not match the user entered."

    interface_app._entry_username_login.delete(0, "end")
    interface_app._entry_password_login.delete(0, "end")

@pytest.mark.usefixtures("mongo_test_db")
def test_login_and_program(interface_app: InterfaceApp) -> None:
    interface_app._entry_username_login.insert(0, USERNAME_MOCK)
    interface_app._entry_password_login.insert(0, PASSWORD_MOCK)

    interface_app._login()

    assert interface_app.user
    assert interface_app.username == interface_app.user.get("username")

    title = interface_app._win_program.title()
    resizable = interface_app._win_program.resizable()
    config_bg = interface_app._win_program.cget("bg")

    assert title == "Program"
    assert resizable == (False, False)
    assert config_bg == PRIMARY_COLOR

    assert interface_app._text_confirm_program.get() == f"Welcome {interface_app.username}"

@pytest.mark.usefixtures("mongo_test_db")
def test_remove_test_user() -> None:
    config = load_config()
    config_mongo = config["mongo"]

    logging.info(f"CONFIG MONGO: {config_mongo}")

    mongo = load_mongo(config=config_mongo)

    db = mongo[config_mongo.get("db_name")]

    db.users.delete_one({
        "username": USERNAME_MOCK
    })