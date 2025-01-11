import subprocess
import logging
import time
from tkinter import Tk

import pytest

from src.app import load_config
from src.app import load_mongo
from src.models.InterfaceApp import InterfaceApp

from test.constants import USERNAME_MOCK
from test.constants import PASSWORD_MOCK


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


@pytest.fixture(scope="session")
def interface_app() -> InterfaceApp:
    root = Tk()

    root.app_config = load_config()
    root.app_mongo = load_mongo(config=root.app_config["mongo"])

    return InterfaceApp(root=root)

# MONGO FIXTURES
@pytest.fixture(scope="session")
def mongo_test_db() -> None:
    subprocess.run(
        ["docker-compose", "up", "-d", "login-db"],
        capture_output=True,
        text=True,
    )

    time.sleep(5)

    yield

    subprocess.run(
        ["docker-compose", "down"],
        capture_output=True,
        text=True,
    )