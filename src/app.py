import os
from tkinter import Tk
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient

from src.data_access.user_dao import UserDAO
from src.services.auth_service import AuthService
from src.ui.interface_app import InterfaceApp


def load_config() -> dict[str, Any]:
    load_dotenv()

    return {
        "mongo": {
            "host": os.getenv("MONGO_HOST"),
            "username": os.getenv("MONGO_USERNAME"),
            "password": os.getenv("MONGO_PASSWORD"),
            "db_name": os.getenv("MONGO_DB_NAME"),
            "auth_source": os.getenv("MONGO_AUTH_SOURCE"),
            "port": os.getenv("MONGO_PORT"),
        }
    }


def load_mongo(config: dict[str, Any]) -> MongoClient:
    username = config.get("username", "")
    password = config.get("password", "")
    host = config.get("host", "")
    port = config.get("port", "")
    db_name = config.get("db_name", "")
    auth_source = config.get("auth_source", "")

    uri = f"mongodb://{username}:{password}@{host}:{port}/{db_name}?authSource={auth_source}"
    return MongoClient(uri)


def main():
    root = Tk()

    app_config = load_config()

    mongo_client = load_mongo(app_config["mongo"])
    db = mongo_client[app_config["mongo"]["db_name"]]

    user_dao = UserDAO(db)
    auth_service = AuthService(user_dao)

    app = InterfaceApp(root=root, auth_service=auth_service)
    root.mainloop()

    print(f"App finalizó: {app}")


if __name__ == "__main__":
    main()
