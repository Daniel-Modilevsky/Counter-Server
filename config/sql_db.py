import sqlite3
import os
from sqlite3 import Cursor, Connection

from config.config_dev import DB_NAME as DEV_DB
from config.config_test import DB_NAME as TEST_DB
from utils.constans import EnvironmentModes

environment = os.environ.get('FLASK_DEBUG', EnvironmentModes['DEVELOPMENT'])


def init_db_connection() -> Cursor:
    if environment == EnvironmentModes['TESTING']:
        connection = sqlite3.connect(TEST_DB)
    else:
        connection = sqlite3.connect(DEV_DB)
    cursor = connection.cursor()
    return cursor


def tear_down(connection: Connection):
    connection.commit()
    connection.close()
