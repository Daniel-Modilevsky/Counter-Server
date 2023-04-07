import sqlite3
import os

from config.config import TestConfig, Config
from utils.constans import EnvironmentModes


environment = os.environ.get('FLASK_DEBUG', EnvironmentModes['DEVELOPMENT'])


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        if environment == EnvironmentModes['TESTING']:
            connection = sqlite3.connect(TestConfig.DB_NAME)
        else:
            connection = sqlite3.connect(Config.DB_NAME)
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
