from utils.constans import INITIAL_COUNTER_VALUE, INITIAL_COUNTER_INDEX, ActionType
import sqlite3


def create_and_init_counter_table_query():
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()
    cursor.execute(f'CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, value INTEGER)')
    cursor.execute(
        f'INSERT OR IGNORE INTO counter (id, value) VALUES ({INITIAL_COUNTER_INDEX}, {INITIAL_COUNTER_VALUE})')
    conn.commit()
    conn.close()


def get_counter_query():
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()
    cursor.execute(f'SELECT value FROM counter WHERE id = {INITIAL_COUNTER_INDEX}')
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return result


def update_counter_query(action_type):
    conn = sqlite3.connect('counter.db')
    cursor = conn.cursor()
    if action_type == ActionType.INCREASE:
        cursor.execute(f'UPDATE counter SET value = value + 1 WHERE id = {INITIAL_COUNTER_INDEX}')
    else:
        cursor.execute(f'UPDATE counter SET value = value - 1 WHERE id = {INITIAL_COUNTER_INDEX}')
    conn.commit()
    conn.close()
    return get_counter_query()

