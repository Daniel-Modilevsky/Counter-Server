import unittest
import sqlite3

from datetime import datetime
from flask import Flask
from unittest.mock import MagicMock, patch
from controllers.controller_metadata import get_filtered_counter_metadata_controller

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True


class TestGetFilteredCounterMetadataController(unittest.TestCase):
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.app_context = app.app_context()
        self.app_context.push()
        self.cursor.execute(
            f'CREATE TABLE IF NOT EXISTS metadata '
            f'(id INTEGER PRIMARY KEY, '
            f'ip_address INET NOT NULL, '
            f'timestamp TIMESTAMP WITH TIME ZONE NOT NULL, '
            f'action_type VARCHAR(8) NOT NULL)')

        # INSERT THE MOCK DATABASE

    def tearDown(self):
        self.app_context.pop()
        self.conn.close()

    @patch('validations.validation_metadata.is_valid_limit', return_value=True)
    @patch('validations.validation_metadata.is_valid_timestamp', return_value=True)
    @patch('validations.validation_metadata.is_valid_ip', return_value=True)
    @patch('validations.validation_metadata.is_valid_action_type', return_value=True)
    @patch('queries.query_metadata.get_filtered_metadata_query',
           return_value=[{'id': 1, 'ip_address': '127.0.0.1', 'timestamp': datetime.now(), 'action_type': 'GET'}])
    def test_get_filtered_counter_metadata_controller(self, mock_is_valid_limit, mock_is_valid_timestamp,
                                                      mock_is_valid_ip,
                                                      mock_is_valid_action_type, mock_get_filtered_metadata_query):
        mock_request = MagicMock()
        mock_request.args.get.return_value = 1
        mock_request.args.__contains__.return_value = True


        with Flask(__name__).test_request_context(
                '/metadata?from_timestamp=2023-04-04T20:32:25.569702&to_timestamp=2023-04-04T20:32:50.479861&ip=127.0.0.1&action_type=GET&limit=10'):
            response = get_filtered_counter_metadata_controller()
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertIn('metadata_list', data)
            metadata_list = data['metadata_list']
            self.assertEqual(len(metadata_list), 0)



if __name__ == '__main__':
    unittest.main()
