import sqlite3

from utils.constans import DB_NAME


def init_db_connection():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    return cursor


def distraction_db_connection(connection):
    connection.commit()
    connection.close()
