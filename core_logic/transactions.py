# File: core_logic/transactions.py
# This is the central transaction handler, routing requests based on a card's funding status and payout type.

from . import validation, security, crypto_payouts
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
        
    # --- CORRECTED LOGIC: Check for payout_type to decide on crypto payout ---
    payout_type = data.get('payout_type')

    if payout_type:
        logger.info(f"Crypto payout requested. Processing as {payout_type}.")
        payout_result = crypto_payouts.make_payout(payout_type, data.get('merchant_wallet'), data.get('amount'), data.get('protocol'))
        database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'crypto_payout', payout_result['status'], payout_result.get('tx_hash'))
        return {"status": payout_result['status'], "message": "Payout initiated", "tx_hash": payout_result.get('tx_hash')}
    else:
        logger.info("No crypto payout requested. Processing with external payment gateway.")
        # Placeholder for calling the payment gateway
        # In a real app, this would route the transaction to a traditional payment processor.
        time.sleep(1) # Simulate API call
        result = {"status": "approved", "transaction_id": f"txn_{int(time.time())}"}
        database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'traditional_sale', result['status'])
        return result


def handle_iso_transaction(iso_data):
    """
    Handles a payment transaction received via the TCP listener.
    """
    logger.info("Handling ISO transaction...")
    
    # --- CORRECTED LOGIC: Check for payout_type to decide on crypto payout ---
    payout_type = iso_data.get('payout_type')

    if payout_type:
        logger.info(f"Crypto payout requested. Processing as {payout_type}.")
        payout_result = crypto_payouts.make_payout(payout_type, iso_data.get('merchant_wallet'), iso_data.get('amount'), iso_data.get('protocol'))
        database.save_transaction(iso_data.get('protocol'), iso_data.get('amount'), iso_data.get('auth_code'), 'crypto_payout', payout_result['status'], payout_result.get('tx_hash'))
        return {"status": payout_result['status'], "message": "Payout initiated", "tx_hash": payout_result.get('tx_hash')}
    else:
        logger.info("No crypto payout requested. Processing with external payment gateway.")
        # Placeholder for calling the payment gateway
        # In a real app, this would route the transaction to a traditional payment processor.
        time.sleep(1) # Simulate API call
        result = {"status": "approved", "transaction_id": f"txn_{int(time.time())}"}
        database.save_transaction(iso_data.get('protocol'), iso_data.get('amount'), iso_data.get('auth_code'), 'traditional_sale', result['status'])
        return result
