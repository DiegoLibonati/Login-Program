import os
from typing import Any
from tkinter import Tk

from dotenv import load_dotenv
from pymongo import MongoClient

from src.models.InterfaceApp import InterfaceApp


def load_config() -> dict[str, Any]:
    load_dotenv()

    mongo_host = os.getenv("MONGO_HOST")
    mongo_username = os.getenv("MONGO_USERNAME")
    mongo_password = os.getenv("MONGO_PASSWORD")
    mongo_db_name = os.getenv("MONGO_DB_NAME")
    mongo_auth_source = os.getenv("MONGO_AUTH_SOURCE")
    mongo_port = os.getenv("MONGO_PORT")

    return {
        "mongo": {
            "host": mongo_host,
            "username": mongo_username,
            "password": mongo_password,
            "db_name": mongo_db_name,
            "auth_source": mongo_auth_source,
            "port": mongo_port,
        }
    }

def load_mongo(config: dict[str, Any]) -> MongoClient:
    username = config.get("username", "")
    password = config.get("password", "")
    host = config.get("host", "")
    db_name = config.get("db_name", "")
    auth_source = config.get("auth_source", "")

    uri = f"mongodb://{username}:{password}@{host}/{db_name}?authSource={auth_source}"
    return MongoClient(uri)

def main():
    root = Tk()

    root.app_config = load_config()
    root.app_mongo = load_mongo(config=root.app_config["mongo"])

    app = InterfaceApp(root=root)
    root.mainloop()

    print(f"App: {app}")


if __name__ == "__main__":
    main()