from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import threading

from config.sql_db import init_db_connection
from controllers.controller_counter import get_counter_controller, increment_controller, decrement_controller
from queries.query_counter import create_and_init_counter_table_query

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///counter.db'
db = SQLAlchemy(app)


class Counter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)


# # Initialize the lock
counter_lock = threading.Lock()

#
# class Counter(db.Model):
#     # id = db.Column(db.Integer, primary_key=True)
#     value = db.Column(db.Integer, nullable=False, primary_key=True, default=0)
#
#     def __repr__(self):
#         return self.value
#
#
# class CounterCallMetadata(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.String(50), nullable=False, default=datetime.utcnow)
#     ip = db.Column(db.String(50), nullable=False, default=DEFAULT_IP)
#     ActionType = db.Column(db.String(10), nullable=False, default=HttpMethod.GET)
#

# initialize counter value to 0
# counter = 0
# cursor = init_db_connection()
create_and_init_counter_table_query()


# Routes
@app.route('/')
def index():
    return 'Welcome to the Counter Service.'


app.route('/get', methods=['GET'])(get_counter_controller)
app.route('/increase', methods=['POST'])(increment_controller)
app.route('/decrease', methods=['POST'])(decrement_controller)


app.run(host='0.0.0.0', port=9090)
