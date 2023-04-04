from enum import Enum


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PATCH = 'PATCH'


class ActionType(Enum):
    INCREASE = 'INCREASE'
    DECREASE = 'DECREASE'


DEFAULT_IP = '127.0.0.1'
INITIAL_COUNTER_VALUE = 0
INITIAL_COUNTER_INDEX = 1
