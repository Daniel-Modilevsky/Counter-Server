from flask import Flask

from controllers.controller_counter import get_counter_controller, increment_controller, decrement_controller
from controllers.controller_metadata import get_filtered_counter_metadata_controller
from queries.query_counter import create_and_init_counter_table_query
from queries.query_metadata import create_and_init_counter_metadata_table_query

app = Flask(__name__)

# Init connections to DB
create_and_init_counter_table_query()
create_and_init_counter_metadata_table_query()


# Routes
@app.route('/')
def index():
    return 'Welcome to the Counter Service.'


app.route('/get', methods=['GET'])(get_counter_controller)
app.route('/increase', methods=['POST'])(increment_controller)
app.route('/decrease', methods=['POST'])(decrement_controller)
app.route('/metadata', methods=['GET'])(get_filtered_counter_metadata_controller)

app.run(host='0.0.0.0', port=5050)
