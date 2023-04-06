import re
import string


def is_not_empty(data: str) -> bool:
    """Check if the data is not empty"""
    return bool(data)


def is_valid_timestamp(timestamp_str: str) -> bool:
    """
    Check if a string is a valid timestamp in the format of 'YYYY-MM-DDThh:mm:ss.ssssss'
    """
    pattern = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{6}$"
    if not re.match(pattern, timestamp_str):
        return False
    return True


def is_valid_ipv4(ip: str) -> bool:
    """
    Returns True if the given string is a valid IPv4 address, else returns False.
    """
    parts = ip.split('.')
    # check that there are exactly 4 parts
    if len(parts) != 4:
        return False
    # check that each part is an integer between 0 and 255
    for part in parts:
        if not part.isdigit():  # check if the part is a digit
            return False
        if len(part) > 1 and part.startswith('0'):  # check if the part starts with 0 but has more digits
            return False
        if not 0 <= int(part) <= 255:  # check if the part is between 0 and 255
            return False
    return True


def is_valid_ipv6(ip: str) -> bool:
    """
    Returns True if the given string is a valid IPv6 address, else returns False.
    """
    parts = ip.split(':')
    # check that there are exactly 8 parts
    if len(parts) != 8:
        return False
    # check that each part is a valid hexadecimal number
    for part in parts:
        # check that the part is not empty and contains only hexadecimal characters
        if not part or not all(c in string.hexdigits for c in part):
            return False
        # check that the integer value of the part is between 0 and 65535
        if not 0 <= int(part, 16) <= 65535:
            return False
    return True


def is_valid_ip(ip: str) -> bool:
    """Check if the IP address is valid"""
    # Compare to IPV4 addresses
    # Compare to IPV6 addresses
    valid_ipv4 = is_valid_ipv4(ip)
    valid_ipv6 = is_valid_ipv6(ip)
    return valid_ipv4 or valid_ipv6


def is_valid_action_type(action_type: str) -> bool:
    """Check if the action type is valid"""
    return action_type in ['GET', 'INCREASE', 'DECREASE']


def is_valid_limit(limit: str) -> bool:
    """Check if the limit is a positive integer"""
    # check that the limit is not empty and contains only digits
    if not limit.isdigit():
        return False
    # convert the limit to an integer and check that it is positive
    limit_int = int(limit)
    return limit_int > 0
