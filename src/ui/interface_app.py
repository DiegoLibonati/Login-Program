from tkinter import Button, Entry, Label, StringVar, Tk, Toplevel

from src.services.auth_service import AuthService
from src.utils.styles import (
    ANCHOR_CENTER,
    FONT_ROBOTO_12,
    FONT_ROBOTO_13,
    FONT_ROBOTO_15,
    PRIMARY_COLOR,
    SECONDARY_COLOR,
    WHITE_COLOR,
)


class InterfaceApp:
    def __init__(
        self, root: Tk, auth_service: AuthService, bg: str = PRIMARY_COLOR
    ) -> None:
        self._root = root
        self._root.title("Login")
        self._root.geometry("400x400")
        self._root.resizable(False, False)
        self._root.config(bg=bg)

        self.auth_service = auth_service
        self.user = None

        self._create_widgets()

    @property
    def username(self) -> str:
        return self.user.get("username", "N/A") if self.user else "N/A"

    def _create_widgets(self) -> None:
        self._text_confirm_login = StringVar(value="Welcome")
        self._text_username_login = StringVar()
        self._text_password_login = StringVar()

        Label(
            self._root,
            text="Username",
            font=FONT_ROBOTO_12,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=90, y=20)
        Entry(
            self._root,
            width=20,
            font=FONT_ROBOTO_15,
            bg=SECONDARY_COLOR,
            border=0,
            fg=WHITE_COLOR,
            textvariable=self._text_username_login,
        ).place(x=200, y=60, anchor=ANCHOR_CENTER)

        Label(
            self._root,
            text="Password",
            font=FONT_ROBOTO_12,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=90, y=80)
        Entry(
            self._root,
            width=20,
            font=FONT_ROBOTO_15,
            show="*",
            bg=SECONDARY_COLOR,
            border=0,
            fg=WHITE_COLOR,
            textvariable=self._text_password_login,
        ).place(x=200, y=120, anchor=ANCHOR_CENTER)

        Label(
            self._root,
            textvariable=self._text_confirm_login,
            font=FONT_ROBOTO_13,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=200, y=255, anchor=ANCHOR_CENTER)

        Button(
            self._root,
            text="Login",
            width=15,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
            command=self._login,
        ).place(x=200, y=300, anchor=ANCHOR_CENTER)
        Button(
            self._root,
            text="Register",
            width=15,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
            command=self._window_register,
        ).place(x=200, y=340, anchor=ANCHOR_CENTER)

    def _login(self) -> None:
        username = self._text_username_login.get()
        password = self._text_password_login.get()
        user, msg = self.auth_service.login(username, password)

        if not user:
            self._text_confirm_login.set(msg)
            return

        self.user = user
        self._program()

    def _window_register(self) -> None:
        self._win_register = Toplevel(self._root)
        self._win_register.title("Register")
        self._win_register.geometry("400x400")
        self._win_register.resizable(False, False)
        self._win_register.config(bg=PRIMARY_COLOR)

        self._text_confirm_register = StringVar()
        self._text_username_register = StringVar()
        self._text_password_register = StringVar()
        self._text_confirm_password_register = StringVar()

        Label(
            self._win_register,
            text="Username",
            font=FONT_ROBOTO_12,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=90, y=20)
        Entry(
            self._win_register,
            width=20,
            font=FONT_ROBOTO_15,
            bg=SECONDARY_COLOR,
            border=0,
            fg=WHITE_COLOR,
            textvariable=self._text_username_register,
        ).place(x=200, y=60, anchor=ANCHOR_CENTER)

        Label(
            self._win_register,
            text="Password",
            font=FONT_ROBOTO_12,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=90, y=80)
        Entry(
            self._win_register,
            width=20,
            font=FONT_ROBOTO_15,
            show="*",
            bg=SECONDARY_COLOR,
            border=0,
            fg=WHITE_COLOR,
            textvariable=self._text_password_register,
        ).place(x=200, y=120, anchor=ANCHOR_CENTER)

        Label(
            self._win_register,
            text="Confirm password",
            font=FONT_ROBOTO_12,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=90, y=140)
        Entry(
            self._win_register,
            width=20,
            font=FONT_ROBOTO_15,
            show="*",
            bg=SECONDARY_COLOR,
            border=0,
            fg=WHITE_COLOR,
            textvariable=self._text_confirm_password_register,
        ).place(x=200, y=180, anchor=ANCHOR_CENTER)

        Label(
            self._win_register,
            textvariable=self._text_confirm_register,
            font=FONT_ROBOTO_13,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=200, y=255, anchor=ANCHOR_CENTER)

        Button(
            self._win_register,
            text="Register",
            width=15,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
            command=self._register,
        ).place(x=200, y=340, anchor=ANCHOR_CENTER)

    def _register(self) -> None:
        ok, msg = self.auth_service.register(
            self._text_username_register.get(),
            self._text_password_register.get(),
            self._text_confirm_password_register.get(),
        )
        self._text_confirm_register.set(msg)
        if ok:
            self._win_register.destroy()

    def _program(self) -> None:
        self._win_program = Toplevel(self._root)
        self._win_program.title("Program")
        self._win_program.geometry("200x200")
        self._win_program.resizable(False, False)
        self._win_program.config(bg=PRIMARY_COLOR)

        msg = f"Welcome {self.username}"
        Label(
            self._win_program,
            text=msg,
            font=FONT_ROBOTO_13,
            bg=PRIMARY_COLOR,
            fg=WHITE_COLOR,
        ).place(x=100, y=100, anchor=ANCHOR_CENTER)
