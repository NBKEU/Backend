# File: database/database.py
# This is a placeholder for your database interaction layer.
# It simulates saving data to a database.

import logging
import time

transactions_db = []
logger = logging.getLogger(__name__)

def save_transaction(protocol, amount, auth_code, transaction_type, status, tx_hash=None):
    """
    Simulates saving a transaction record to the database.
    """
    transaction = {
        "protocol": protocol,
        "amount": amount,
        "auth_code": auth_code,
        "transaction_type": transaction_type,
        "status": status,
        "timestamp": time.time(),
        "tx_hash": tx_hash
    }
    transactions_db.append(transaction)
    logger.info(f"Transaction saved to DB: {transaction}")
    return True

def get_transaction_history():
    return transactions_db
