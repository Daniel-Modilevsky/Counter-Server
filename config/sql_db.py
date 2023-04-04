import sqlite3


def init_db_connection():
    connection = sqlite3.connect('counter.db')
    cursor = connection.cursor()
    return cursor


def distraction_db_connection(connection):
    connection.commit()
    connection.close()
