from decorators.decorator_db import with_db_connection
from tests.mock_metadata import mock_metadata_table


@with_db_connection
def initial_test_metadata_db_query(cursor):
    for index in range(len(mock_metadata_table)):
        cursor.execute("""INSERT INTO metadata(timestamp, ip_address, action_type) 
                       VALUES (?,?,?);""", (
            mock_metadata_table[index]["timestamp"], mock_metadata_table[index]["ip_address"],
            mock_metadata_table[index]["action_type"]))


@with_db_connection
def remove_metadata_db_query(cursor):
    cursor.execute(f'DROP TABLE metadata')
