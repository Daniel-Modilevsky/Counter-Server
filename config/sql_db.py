import sqlite3
import os
from sqlite3 import Cursor, Connection
from config import *
from utils.constans import EnvironmentModes

environment = os.environ.get('FLASK_DEBUG', EnvironmentModes['DEVELOPMENT'])


def init_db_connection() -> Cursor:
    if environment == EnvironmentModes['TESTING']:
        connection = sqlite3.connect(TestConfig.DB_NAME)
    else:
        connection = sqlite3.connect(Config.DB_NAME)
    cursor = connection.cursor()
    return cursor


def tear_down(connection: Connection):
    connection.commit()
    connection.close()
