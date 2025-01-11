# coding: utf8
from typing import Any
from tkinter import Tk
from tkinter import StringVar
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Toplevel

from pymongo import MongoClient
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from src.utils.constants import PRIMARY_COLOR
from src.utils.constants import SECONDARY_COLOR
from src.utils.constants import WHITE_COLOR
from src.utils.constants import FONT_ROBOTO_12
from src.utils.constants import FONT_ROBOTO_13
from src.utils.constants import FONT_ROBOTO_15
from src.utils.constants import ANCHOR_CENTER


class InterfaceApp:
    def __init__(self, root: Tk, bg: str = PRIMARY_COLOR) -> None:
        # APP Config
        self._root = root
        self._root.title("Login")
        self._root.geometry("400x400")
        self._root.resizable(False, False)
        self._root.config(bg=bg)

        self.user = None

        # Create widges
        self._create_widgets()


    @property
    def config_mongo(self) -> dict[str, Any]:
        return self._root.app_config["mongo"]

    @property
    def db(self) -> MongoClient:
        db_name = self.config_mongo.get("db_name")
        return self._root.app_mongo[db_name]
    
    @property
    def username(self) -> str:
        return self.user.get("username", "N/A") if self.user else "N/A"

    def _create_widgets(self) -> None:
        self._text_confirm_login = StringVar(value="Welcome")
        self._text_username_login = StringVar()
        self._text_password_login = StringVar()

        self._label_username_login = Label(master=self._root, text="Username", font=FONT_ROBOTO_12, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_username_login.place(x=90, y=20)

        self._entry_username_login = Entry(master=self._root, width=20, font=FONT_ROBOTO_15, bg=SECONDARY_COLOR, border=0, fg=WHITE_COLOR, textvariable=self._text_username_login)
        self._entry_username_login.place(x=200, y=60, anchor=ANCHOR_CENTER)

        self._label_password_login = Label(master=self._root, text="Password", font=FONT_ROBOTO_12, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_password_login.place(x=90, y=80)

        self._entry_password_login = Entry(master=self._root, width=20, font=FONT_ROBOTO_15, show="*", bg=SECONDARY_COLOR, border=0, fg=WHITE_COLOR, textvariable=self._text_password_login)
        self._entry_password_login.place(x=200, y=120, anchor=ANCHOR_CENTER)

        self._label_confirm_login = Label(master=self._root, textvariable=self._text_confirm_login, font=FONT_ROBOTO_13, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_confirm_login.place(x=200, y=255, anchor=ANCHOR_CENTER)

        Button(master=self._root, text="Login", width=15, bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=lambda:self._login()).place(x=200, y=300, anchor=ANCHOR_CENTER)
        Button(master=self._root, text="Register", width=15, bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=lambda:self._window_register()).place(x=200, y=340, anchor=ANCHOR_CENTER)

    def _window_register(self) -> None:
        self._win_register = Toplevel()
        self._win_register.title('Register')
        self._win_register.geometry('400x400')
        self._win_register.resizable(False, False)
        self._win_register.config(bg=PRIMARY_COLOR)

        self._text_confirm_register = StringVar()
        self._text_username_register = StringVar()
        self._text_password_register = StringVar()
        self._text_confirm_password_register = StringVar()

        self._label_username_register = Label(master=self._win_register, text="Username", font=FONT_ROBOTO_12, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_username_register.place(x=90, y=20)

        self._entry_username_register = Entry(master=self._win_register, width=20, font=FONT_ROBOTO_15, bg=SECONDARY_COLOR, border=0, fg=WHITE_COLOR, textvariable=self._text_username_register)
        self._entry_username_register.place(x=200, y=60, anchor=ANCHOR_CENTER)

        self._label_password_register = Label(master=self._win_register, text="Password", font=FONT_ROBOTO_12, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_password_register.place(x=90, y=80)

        self._entry_password_register = Entry(master=self._win_register, width=20, font=FONT_ROBOTO_15, show="*", bg=SECONDARY_COLOR, border=0, fg=WHITE_COLOR, textvariable=self._text_password_register)
        self._entry_password_register.place(x=200, y=120, anchor=ANCHOR_CENTER)

        self._label_confirm_password_register = Label(master=self._win_register, text="Confirm password", font=FONT_ROBOTO_12, bg=PRIMARY_COLOR, fg=WHITE_COLOR)
        self._label_confirm_password_register.place(x=90, y=140)

        self._entry_confirm_password_register = Entry(master=self._win_register, width=20, font=FONT_ROBOTO_15, show="*", bg=SECONDARY_COLOR, border=0, fg=WHITE_COLOR, textvariable=self._text_confirm_password_register)
        self._entry_confirm_password_register.place(x=200, y=180, anchor=ANCHOR_CENTER)

        Label(master=self._win_register, textvariable=self._text_confirm_register, font=FONT_ROBOTO_13, bg=PRIMARY_COLOR, fg=WHITE_COLOR).place(x=200, y=255, anchor=ANCHOR_CENTER)

        Button(master=self._win_register, text="Register", width=15, bg=PRIMARY_COLOR, fg=WHITE_COLOR, command=lambda:self._register()).place(x=200, y=340, anchor=ANCHOR_CENTER)

    def _login(self) -> None:
        username = self._entry_username_login.get()
        password = self._entry_password_login.get()

        self.user = self.db.users.find_one({"username": username})

        if not self.user:
            self._text_confirm_login.set("The entered username does not exist in our database.")
            return
        
        db_password = self.user["password"]

        if not check_password_hash(db_password, password):
            self._text_confirm_login.set("The password does not match the user entered.")
            return
            
        self._program()

    def _register(self) -> None:
        username = self._entry_username_register.get()
        password = self._entry_password_register.get()
        confirm_password = self._entry_confirm_password_register.get()
        
        if not username or not password or not confirm_password or username.isspace() or password.isspace() or confirm_password.isspace():
            self._text_confirm_register.set("You must enter valid fields.")
            return

        if password != confirm_password:
            self._text_confirm_register.set("The passwords entered do not match.")
            return
        
        user = {
            "username": username,
            "password": generate_password_hash(password)
        }

        self.db.users.insert_one(user)
        self._text_confirm_register.set("The user was successfully created.")
        self._win_register.destroy()

    def _program(self) -> None:
        self._win_program = Toplevel()
        self._win_program.title('Program')
        self._win_program.geometry('200x200')
        self._win_program.resizable(False, False)
        self._win_program.config(bg=PRIMARY_COLOR)

        self._text_confirm_program = StringVar(value=f"Welcome {self.username}")

        Label(master=self._win_program, textvariable=self._text_confirm_program, font=FONT_ROBOTO_13, bg=PRIMARY_COLOR, fg=WHITE_COLOR).place(x=100, y=100, anchor=ANCHOR_CENTER)