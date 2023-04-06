# When writing unit tests for Flask applications with SQLite,
# it's common to use an in-memory SQLite database instead of connecting to a real database.
# This approach is faster and ensures that your tests are isolated from your development database.
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<User {self.name}>'


@app.route('/users')
def get_users():
    users = User.query.all()
    user_list = [{'id': u.id, 'name': u.name} for u in users]
    return jsonify(user_list)


class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
        db.session.add(User(name='Alice'))
        db.session.add(User(name='Bob'))
        db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_get_users(self):
        with app.test_client() as client:
            response = client.get('/users')
            data = response.get_json()

            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['name'], 'Alice')
            self.assertEqual(data[1]['name'], 'Bob')


if __name__ == '__main__':
    unittest.main()


class MetadataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()
        # db.session.add(User(name='Alice'))
        # db.session.add(User(name='Bob'))
        # db.session.commit()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()

    def setUp(self):
        self.client = app.test_client()

    def test_get_filtered_counter_metadata_controller(self):
        with patch('app.request') as mock_request:
            mock_request.args.get.side_effect = lambda key, default=None: {
                'page': 1,
                'from_timestamp': '2023-04-04T20:32:00.000000',
                'to_timestamp': '2023-04-04T20:33:00.000000',
                'ip': '127.0.0.1',
                'action_type': 'INCREASE',
                'limit': None
            }.get(key, default)

            with patch('app.get_filtered_metadata_query') as mock_query:
                mock_query.return_value = [
                    {'id': 2, 'ip_address': '127.0.0.1', 'timestamp': '2023-04-04 20:32:44.599130',
                     'action_type': 'INCREASE'},
                    {'id': 3, 'ip_address': '127.0.0.1', 'timestamp': '2023-04-04 20:32:50.479861',
                     'action_type': 'INCREASE'}
                ]

                response = self.client.get('/metadata')
                self.assertEqual(response.status_code, 200)

                data = response.get_json()
                self.assertIsInstance(data, dict)
                self.assertIn('metadata_list', data)
                metadata_list = data['metadata_list']
                self.assertIsInstance(metadata_list, list)
                self.assertEqual(len(metadata_list), 2)
                self.assertEqual(metadata_list[0]['id'], 2)
                self.assertEqual(metadata_list[0]['ip_address'], '127.0.0.1')
                self.assertEqual(metadata_list[0]['timestamp'], '2023-04-04 20:32:44.599130')
                self.assertEqual(metadata_list[0]['action_type'], 'INCREASE')
                self.assertEqual(metadata_list[1]['id'], 3)
                self.assertEqual(metadata_list[1]['ip_address'], '127.0.0.1')
                self.assertEqual(metadata_list[1]['timestamp'], '2023-04-04 20:32:50.479861')
                self.assertEqual(metadata_list[1]['action_type'], 'INCREASE')

            mock_query.assert_called_once_with('INCREASE', '2023-04-04T20:32:00.000000', '2023-04-04T20:33:00.000000',
                                               '127.0.0.1')

        with patch('app.request') as mock_request:
            mock_request.args.get.side_effect = lambda key, default=None: {
                'page': 1,
                'from_timestamp': '2023-04-04T20:32:00.000000',
                'to_timestamp': '2023-04-04T20:33:00.000000',
                'ip': '127.0.0.1',
                'action_type': 'INVALID_ACTION_TYPE',
                'limit': None
            }.get(key, default)

# We're creating a new Flask application instance with the TESTING configuration set to True.
# We're also using an in-memory SQLite database
# by setting the SQLALCHEMY_DATABASE_URI configuration to 'sqlite:///:memory:'.
#
# In the setUp method, we're creating all the necessary database tables using the db.create_all() method.
# In the tearDown method, we're removing the database session and dropping all the database tables.
#
# Finally, in the test_my_function method, we're inserting test data into the database,
# calling our function, and asserting the result.
# By using an in-memory SQLite database, your tests will run faster,
# and be more isolated from your development database.
