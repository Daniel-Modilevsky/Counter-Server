from time import strftime

from decorators.decorator_db import with_db_connection
from utils.constans import TableNames, MINIMUM_LIMIT


@with_db_connection
def create_and_init_counter_metadata_table_query(cursor):
    cursor.execute(
        f'CREATE TABLE IF NOT EXISTS metadata '
        f'(id INTEGER PRIMARY KEY, '
        f'ip_address INET NOT NULL, '
        f'timestamp TIMESTAMP WITH TIME ZONE NOT NULL, '
        f'action_type VARCHAR(8) NOT NULL)')


@with_db_connection
def get_filtered_metadata_query(cursor, action_type=None, from_timestamp=None, to_timestamp=None, ip_address=None,
                                limit=MINIMUM_LIMIT):
    query = f'SELECT * FROM {TableNames["METADATA"]}'
    filters = []
    if action_type:
        filters.append(f"action_type='{action_type}'")
    if from_timestamp:
        filters.append(f"timestamp > '{from_timestamp}'")
    if to_timestamp:
        filters.append(f"timestamp < '{to_timestamp}'")
    if ip_address:
        filters.append(f"ip_address='{ip_address}'")

    if filters:
        query += " WHERE " + " AND ".join(filters)

    query += f" LIMIT {limit}"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


@with_db_connection
def get_last_metadata_query(cursor):
    # return new metadata by order by timestamp bottom up and return the first
    cursor.execute(f'SELECT * FROM {TableNames["METADATA"]} ORDER BY id DESC LIMIT 1')
    result = cursor.fetchone()
    return result


@with_db_connection
def insert_metadata_query(cursor, action_type, timestamp, ip_address):
    cursor.execute("""INSERT INTO metadata(timestamp, ip_address, action_type) 
                   VALUES (?,?,?);""", (strftime(timestamp), ip_address, action_type))
    return get_last_metadata_query()
