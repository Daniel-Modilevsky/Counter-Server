from datetime import datetime
import sqlite3
from flask import request


def insert_audit_log(action):
    # get timestamp and IP address of requester
    timestamp = datetime.datetime.now().isoformat()
    ip_address = request.remote_addr
    # insert record into audit_log table
    conn = sqlite3.connect('counter.db')
    c = conn.cursor()
    c.execute("INSERT INTO audit_log VALUES (?, ?, ?, ?)", (timestamp, ip_address, action, ''))
    conn.commit()
    conn.close()