import sqlite3
import os
from utils.constans import EnvironmentModes
from config.config_dev import DB_NAME as DEV_DB
from config.config_test import DB_NAME as TEST_DB

environment = os.environ.get('FLASK_DEBUG', EnvironmentModes['DEVELOPMENT'])


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        if environment == EnvironmentModes['TESTING']:
            connection = sqlite3.connect(TEST_DB)
        else:
            connection = sqlite3.connect(DEV_DB)
        cursor = connection.cursor()
        result = func(cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return result
    return wrapper
