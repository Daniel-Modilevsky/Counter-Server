from enum import Enum


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


ActionType = {
    "INCREASE": "INCREASE",
    "DECREASE": "DECREASE",
    "GET": "GET"
}

TableNames = {
    "COUNTER": "counter",
    "METADATA": "metadata",
}

DEFAULT_IP = '127.0.0.1'
INITIAL_COUNTER_VALUE = 0
INITIAL_COUNTER_INDEX = 1
DB_NAME = 'counter.db'
MINIMUM_LIMIT = 20
