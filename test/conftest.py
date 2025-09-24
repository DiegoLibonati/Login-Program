import logging
import subprocess
import time
from collections.abc import Generator
from tkinter import Tk
from tkinter import Tk as TkType

import pytest
from pymongo import MongoClient
from pymongo.database import Database

from src.app import load_config, load_mongo
from src.data_access.user_dao import UserDAO
from src.services.auth_service import AuthService
from src.ui.interface_app import InterfaceApp

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


@pytest.fixture(scope="session")
def mongo_test_db() -> Generator[None, None, None]:
    subprocess.run(
        ["docker-compose", "-f", "dev.docker-compose.yml", "up", "-d", "login-db"],
        capture_output=True,
        text=True,
        check=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "-f", "dev.docker-compose.yml", "down"],
        capture_output=True,
        text=True,
        check=True,
    )


@pytest.fixture
def mongo_db(mongo_test_db: None) -> Generator[Database, None, None]:
    config: dict[str, dict[str, str]] = load_config()

    mongo_client: MongoClient = load_mongo(config["mongo"])
    db: Database = mongo_client[config["mongo"]["db_name"]]

    db.users.delete_many({})

    yield db

    db.users.delete_many({})


@pytest.fixture
def interface_app(mongo_db: Database) -> Generator[InterfaceApp, None, None]:
    root: TkType = Tk()

    user_dao: UserDAO = UserDAO(mongo_db)
    auth_service: AuthService = AuthService(user_dao)

    app: InterfaceApp = InterfaceApp(root=root, auth_service=auth_service)

    yield app

    root.destroy()
