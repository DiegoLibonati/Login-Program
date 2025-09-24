from test.constants import PASSWORD_MOCK, USERNAME_MOCK
from tkinter import Tk

from src.ui.interface_app import InterfaceApp
from src.utils.styles import PRIMARY_COLOR


def test_initial_config_tk_app(interface_app: InterfaceApp) -> None:
    root: Tk = interface_app._root
    root.update()

    assert root.title() == "Login"
    assert root.geometry().split("+")[0] == "400x400"
    assert root.resizable() == (False, False)
    assert root.cget("bg") == PRIMARY_COLOR
    assert interface_app.username == "N/A"
    assert interface_app.user is None


def test_create_widgets(interface_app: InterfaceApp) -> None:
    interface_app._create_widgets()

    assert interface_app._text_confirm_login.get() == "Welcome"
    assert interface_app._text_username_login.get() == ""
    assert interface_app._text_password_login.get() == ""


def test_window_register(interface_app: InterfaceApp) -> None:
    interface_app._window_register()
    win: Tk = interface_app._win_register

    assert win.title() == "Register"
    assert win.resizable() == (False, False)
    assert win.cget("bg") == PRIMARY_COLOR

    assert interface_app._text_confirm_register.get() == ""


def test_register_and_login(interface_app: InterfaceApp) -> None:
    interface_app._window_register()

    interface_app._text_username_register.set(USERNAME_MOCK)
    interface_app._text_password_register.set(PASSWORD_MOCK)
    interface_app._text_confirm_password_register.set(PASSWORD_MOCK)

    interface_app._register()
    assert (
        interface_app._text_confirm_register.get()
        == "The user was successfully created."
    )

    interface_app._text_username_login.set(USERNAME_MOCK)
    interface_app._text_password_login.set(PASSWORD_MOCK)

    interface_app._login()
    assert interface_app.user
    assert interface_app.username == USERNAME_MOCK
    assert interface_app._win_program.title() == "Program"
