import unittest
import sqlite3
from datetime import datetime

from queries.query_counter_metadata import get_filtered_metadata_query
from tests.mock_metadata import mock_metadata_table
from tests.mock_metadata_query import initial_test_metadata_db_query

# Init test db metadata
# initial_test_metadata_db_query()


class TestMetadataFunctions(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(':memory:')
        self.cursor = self.conn.cursor()
        self.create_table_query = '''CREATE TABLE metadata
            (id INTEGER PRIMARY KEY,
             timestamp TEXT NOT NULL,
             ip_address TEXT NOT NULL,
             action_type TEXT NOT NULL);'''
        self.cursor.execute(self.create_table_query)
        self.mock_data = mock_metadata_table

        for row in self.mock_data:
            timestamp = datetime.fromisoformat(row['timestamp'])
            self.cursor.execute("INSERT INTO metadata (id, timestamp, ip_address, action_type) VALUES (?, ?, ?, ?)",
                                (row['id'], timestamp, row['ip_address'], row['action_type']))
        # self.conn.commit()

        result = get_filtered_metadata_query(self.cursor, 'INCREASE')
        expected = [(2, '2023-04-04 20:32:44.599130', '127.0.0.1', 'INCREASE'),
                    (3, '2023-04-04 20:32:50.479861', '127.0.0.1', 'INCREASE')]
        self.assertEqual(result, expected)

        result = get_filtered_metadata_query(self.cursor, from_timestamp='2023-04-04T20:32:45.000000')
        expected = [(3, '2023-04-04 20:32:50.479861', '127.0.0.1', 'INCREASE'),
                    (4, '2023-04-04 20:32:51.750759', '127.0.0.1', 'DECREASE')]
        self.assertEqual(result, expected)

        self.cursor.execute("DROP TABLE metadata")
        self.conn.close()

    def tearDown(self):
        self.cursor.execute("DROP TABLE metadata")
        self.conn.close()

    def test_get_filtered_metadata_query(self):
        # Test filtering by action_type
        result = get_filtered_metadata_query(self.cursor)
        expected = [(2, '2023-04-04 20:32:44.599130', '127.0.0.1', 'INCREASE'),
                    (3, '2023-04-04 20:32:50.479861', '127.0.0.1', 'INCREASE')]
        self.assertEqual(result, expected)

        # Test filtering by from_timestamp
        result = get_filtered_metadata_query(self.cursor, from_timestamp='2023-04-04T20:32:45.000000')
        expected = [(3, '2023-04-04 20:32:50.479861', '127.0.0.1', 'INCREASE'),
                    (4, '2023-04-04 20:32:51.750759', '127.0.0.1', 'DECREASE')]
        self.assertEqual(result, expected)

        # Test filtering by to_timestamp
        result = get_filtered_metadata_query(self.cursor, to_timestamp='2023-04-04T20:32:26.000000')
        expected = [(1, '2023-04-04 20:32:25.569702', '127.0.0.1', 'GET')]
        self.assertEqual(result, expected)

        # Test filtering by ip_address
        # result = get_filtered_metadata_query
