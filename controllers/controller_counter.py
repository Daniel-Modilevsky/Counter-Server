from flask import jsonify
import threading

from queries.query_counter import update_counter_query, get_counter_query
from utils.constans import ActionType

# Initialize the lock
counter_lock = threading.Lock()


def get_counter_controller():
    with counter_lock:
        # Validation?
        # Update the log
        # insert_audit_log(request.remote_addr, 'get', counter)
        counter = get_counter_query()
        return jsonify({'counter': counter})


def increment_controller():
    with counter_lock:
        # Validation?
        # Update the log
        # insert_audit_log(request.remote_addr, 'increase', counter)
        counter = update_counter_query(ActionType.INCREASE)
        return jsonify({'counter': counter})


def decrement_controller():
    with counter_lock:
        # Validation?
        # Update the log
        # insert_audit_log(request.remote_addr, 'decrease', counter)
        counter = update_counter_query(ActionType.DECREASE)
        return jsonify({'counter': counter})
