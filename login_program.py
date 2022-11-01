from tkinter import *
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from time import sleep

root = Tk()
root.title('Login')
root.geometry('400x400')
root.config(bg="#141B41")
root.resizable(False, False)

client = MongoClient()
db = client.login_app

confirm_text_label = StringVar(value="Welcome")
entry_user = StringVar()
password_user = StringVar()

user_label = Label(root,text="User", font=("Roboto 12"), bg="#141B41", fg="#fff")
user_label.place(x=90, y=20)

user_entry = Entry(root,width=20, font=("Roboto 15"), bg="#306BAC", border=0, fg="#fff",textvariable=entry_user)
user_entry.place(x=200, y=60, anchor="center")

password_label = Label(root,text="Password", font=("Roboto 12"), bg="#141B41", fg="#fff")
password_label.place(x=90, y=80)

password_entry = Entry(root,width=20, font=("Roboto 15"), show="*", bg="#306BAC", border=0, fg="#fff",textvariable=password_user)
password_entry.place(x=200, y=120, anchor="center")

Label(root, textvariable=confirm_text_label, font=("Roboto 13"), bg="#141B41", fg="#fff").place(x=200, y=255, anchor="center")

Button(root,text="Login", width=15, bg="#141B41", fg="#fff", command=lambda:login()).place(x=200, y=300, anchor="center")
Button(root,text="Register", width=15, bg="#141B41", fg="#fff", command=lambda:window_register()).place(x=200, y=340, anchor="center")

def window_register():
    win = Toplevel()
    win.title('Register')
    win.geometry('400x400')
    win.config(bg="#141B41")
    win.resizable(False, False)

    confirm_text_label = StringVar()
    entry_user = StringVar()
    password_user = StringVar()
    confirm_password_user = StringVar()

    user_label = Label(win,text="User", font=("Roboto 12"), bg="#141B41", fg="#fff")
    user_label.place(x=90, y=20)

    user_entry = Entry(win,width=20, font=("Roboto 15"), bg="#306BAC", border=0, fg="#fff", textvariable=entry_user)
    user_entry.place(x=200, y=60, anchor="center")

    password_label = Label(win,text="Password", font=("Roboto 12"), bg="#141B41", fg="#fff")
    password_label.place(x=90, y=80)

    password_entry = Entry(win,width=20, font=("Roboto 15"), show="*", bg="#306BAC", border=0, fg="#fff", textvariable=password_user)
    password_entry.place(x=200, y=120, anchor="center")

    password_confirm_label = Label(win,text="Confirm password", font=("Roboto 12"), bg="#141B41", fg="#fff")
    password_confirm_label.place(x=90, y=140)

    password_confirm_entry = Entry(win,width=20, font=("Roboto 15"), show="*", bg="#306BAC", border=0, fg="#fff", textvariable=confirm_password_user)
    password_confirm_entry.place(x=200, y=180, anchor="center")

    Label(win, textvariable=confirm_text_label, font=("Roboto 13"), bg="#141B41", fg="#fff").place(x=200, y=255, anchor="center")

    Button(win,text="Register", width=15, bg="#141B41", fg="#fff", command=lambda:register()).place(x=200, y=340, anchor="center")

    def register():
        user = entry_user.get()
        password = password_user.get()
        confirm_password = confirm_password_user.get()
        
        if not user and not user.isspace():
            confirm_text_label.set("Invalid user.")
        elif password != confirm_password:
            confirm_text_label.set("Passwords dont match.")
        else:
            new_user = {"user": user, "password":generate_password_hash(password)}
            db.users.insert_one(new_user)
            confirm_text_label.set("Your user was created.")
            sleep(5)
            win.destroy()

def login():
    user = entry_user.get()
    password = password_user.get()

    db_user = db.users.find_one({"user":user})

    if db_user == None:
        confirm_text_label.set("Invalid user")
    else:
        if check_password_hash(db_user['password'], password):
            program(db_user["user"])
        else:
            confirm_text_label.set("Invalid password")

def program(user):
    win = Toplevel()
    win.title('Program')
    win.geometry('200x200')
    win.config(bg="#141B41")
    win.resizable(False, False)

    confirm_text_label = StringVar(value=f"Welcome {user}")

    Label(win, textvariable=confirm_text_label, font=("Roboto 13"), bg="#141B41", fg="#fff").place(x=100, y=100, anchor="center")

root.mainloop()