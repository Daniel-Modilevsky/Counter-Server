from datetime import datetime
from flask import request, jsonify

from queries.query_counter_metadata import get_filtered_metadata_query, insert_metadata_query
from utils.constans import MINIMUM_LIMIT


def get_filtered_counter_metadata_controller():
    # params validation
    #  If a parameter is not present in the request, get() will return None.
    from_timestamp = request.args.get('from_timestamp')
    to_timestamp = request.args.get('to_timestamp')
    ip_address = request.args.get('ip')
    action_type = request.args.get('action_type')
    limit = request.args.get('limit')
    if limit is None:
        limit = MINIMUM_LIMIT
    metadata_list = get_filtered_metadata_query(action_type, from_timestamp, to_timestamp, ip_address, limit)
    return jsonify({'metadata_list': metadata_list})


def insert_metadata(action):
    # get timestamp and IP address of requester
    timestamp = datetime.now().isoformat()
    ip_address = request.remote_addr
    # insert record into metadata table
    metadata = insert_metadata_query(action, timestamp, ip_address)
    return jsonify({'metadata': metadata})
