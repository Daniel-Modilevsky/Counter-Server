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
        # Check if the metadata table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='metadata'")
        result = cursor.fetchone()
        if not result:
            # Create the metadata table if it doesn't exist
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS metadata '
                f'(id INTEGER PRIMARY KEY, '
                f'ip_address INET NOT NULL, '
                f'timestamp TIMESTAMP WITH TIME ZONE NOT NULL, '
                f'action_type VARCHAR(8) NOT NULL)')

        result = func(cursor, *args, **kwargs)
        connection.commit()
        connection.close()
        return result

    return wrapper
