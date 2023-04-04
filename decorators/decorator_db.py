import sqlite3


def with_db_connection(func):
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('counter.db')
        cursor = conn.cursor()
        result = func(cursor, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
    return wrapper
