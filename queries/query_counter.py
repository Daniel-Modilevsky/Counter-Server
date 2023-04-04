from decorators.decorator_db import with_db_connection
from utils.constans import INITIAL_COUNTER_VALUE, INITIAL_COUNTER_INDEX, ActionType


@with_db_connection
def create_and_init_counter_table_query(cursor):
    cursor.execute(f'CREATE TABLE IF NOT EXISTS counter (id INTEGER PRIMARY KEY, value INTEGER)')
    cursor.execute(
        f'INSERT OR IGNORE INTO counter (id, value) VALUES ({INITIAL_COUNTER_INDEX}, {INITIAL_COUNTER_VALUE})')


@with_db_connection
def get_counter_query(cursor):
    cursor.execute(f'SELECT value FROM counter WHERE id = {INITIAL_COUNTER_INDEX}')
    result = cursor.fetchone()[0]
    return result


@with_db_connection
def update_counter_query(cursor, action_type):
    if action_type == ActionType.INCREASE:
        cursor.execute(f'UPDATE counter SET value = value + 1 WHERE id = {INITIAL_COUNTER_INDEX}')
    else:
        cursor.execute(f'UPDATE counter SET value = value - 1 WHERE id = {INITIAL_COUNTER_INDEX}')
    return get_counter_query()

