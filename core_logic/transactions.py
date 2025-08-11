# File: core_logic/transactions.py
# This is the central transaction handler, routing requests based on protocol.

from . import validation, protocol_mapping, security, crypto_payouts
from database import database
import time
import logging

logger = logging.getLogger(__name__)

def handle_http_transaction(data):
    """
    Handles a payment transaction received via the Flask web API.
    """
    logger.info("Handling HTTP transaction...")
    
    # Basic validation
    if not (validation.validate_amount(data.get('amount')) and
            validation.validate_auth_code(data.get('auth_code'), data.get('protocol'))):
        return {"status": "declined", "message": "Validation failed"}

    # Determine if the transaction is onledger or offledger
    if protocol_mapping.is_onledger_transaction(data.get('protocol')):
        return handle_onledger_transaction(data)
    else:
        return handle_offledger_transaction(data)

def handle_iso_transaction(iso_data):
    """
    Handles a payment transaction received via the TCP listener.
    """
    # In a real app, this would parse the ISO message into a dictionary
    logger.info("Handling ISO transaction...")
    
    # Assuming iso_data is already a dictionary for this example
    if protocol_mapping.is_onledger_transaction(iso_data.get('protocol')):
        return handle_onledger_transaction(iso_data)
    else:
        return handle_offledger_transaction(iso_data)

def handle_onledger_transaction(data):
    """
    Processes an M1 transaction by calling the external payment gateway.
    """
    logger.info("Processing M1 (onledger) transaction...")
    # Placeholder for calling the payment gateway
    # from integration_layer import payment_gateway_service
    # result = payment_gateway_service.process(data)
    time.sleep(1) # Simulate API call
    result = {"status": "approved", "transaction_id": f"txn_{int(time.time())}"}
    
    # Save the transaction to the database
    database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'onledger', result['status'])
    
    return result

def handle_offledger_transaction(data):
    """
    Processes an MO transaction by initiating an in-house crypto payout.
    """
    logger.info("Processing MO (offledger) transaction...")
    
    # In-house crypto payout
    # You need a way to get the merchant's crypto address for the payout
    payout_result = crypto_payouts.make_payout(data.get('payout_type'), data.get('merchant_wallet'), data.get('amount'), data.get('protocol'))
    
    # Save the transaction to the database, including the crypto hash
    database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'offledger', payout_result['status'], payout_result.get('tx_hash'))
    
    return {"status": payout_result['status'], "message": "Payout initiated"}
