from datetime import datetime
from flask import request, jsonify, abort

from queries.query_counter_metadata import get_filtered_metadata_query, insert_metadata_query
from utils.constans import MINIMUM_LIMIT
from validations.validation_metadata_counter import is_valid_limit, is_valid_timestamp, is_valid_action_type, \
    is_valid_ip


def get_filtered_counter_metadata_controller():
    #  If a parameter is not present in the request, get() will return None.
    # Extract params from the request
    from_timestamp = request.args.get('from_timestamp')
    to_timestamp = request.args.get('to_timestamp')
    ip_address = request.args.get('ip')
    action_type = request.args.get('action_type')
    limit = request.args.get('limit')
    if limit is None:
        limit = MINIMUM_LIMIT

    # Validations
    if not is_valid_limit(limit):
        abort(409, 'Invalid to_timestamp parameter')
    if from_timestamp is not None and not is_valid_timestamp(from_timestamp):
        abort(409, 'Invalid from_timestamp parameter')
    if to_timestamp is not None and not is_valid_timestamp(to_timestamp):
        abort(409, 'Invalid to_timestamp parameter')
    if ip_address is not None and not is_valid_ip(ip_address):
        abort(409, 'Invalid ip_address parameter')
    if action_type is not None and not is_valid_action_type(action_type):
        abort(409, 'Invalid action_type parameter')

    metadata_list = get_filtered_metadata_query(action_type, from_timestamp, to_timestamp, ip_address, limit)
    return jsonify({'metadata_list': metadata_list})


def insert_metadata(action: str):
    # get timestamp and IP address of requester
    timestamp = datetime.now().isoformat()
    ip_address = request.remote_addr

    metadata = insert_metadata_query(action, timestamp, ip_address)
    return jsonify({'metadata': metadata})
