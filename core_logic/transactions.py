# File: core_logic/transactions.py
# This is the central transaction handler, routing requests based on card's funds.

from . import validation, protocol_mapping, security, crypto_payouts
from database import database
import time
import logging

logger = logging.getLogger(__name__)

# --- New function to check card funds ---
def _check_card_funds(card_number):
    """
    Simulates checking the funds loaded on a debit card.
    In a real production system, this would involve a live check with your card issuer.
    """
    # Placeholder logic: for demo purposes, we'll assume a card with an even number
    # of digits has funds for an onledger transaction (M1).
    if len(card_number.replace(' ', '')) % 2 == 0:
        return 'funded'  # This will trigger an M1 (onledger) transaction
    else:
        return 'insufficient' # This will trigger an M0 (offledger) transaction


def handle_http_transaction(data):
    """
    Handles a payment transaction received via the Flask web API.
    """
    logger.info("Handling HTTP transaction...")
    
    # Basic validation
    if not (validation.validate_amount(data.get('amount')) and
            validation.validate_auth_code(data.get('auth_code'), data.get('protocol'))):
        return {"status": "declined", "message": "Validation failed"}
        
    # --- Corrected Logic: Determine transaction type based on card funds ---
    card_status = _check_card_funds(data.get('card_number'))

    if card_status == 'funded':
        logger.info("Card has sufficient funds. Processing as M1 (onledger) transaction.")
        return handle_onledger_transaction(data)
    else:
        logger.info("Card has insufficient funds. Processing as M0 (offledger) transaction.")
        return handle_offledger_transaction(data)


def handle_iso_transaction(iso_data):
    """
    Handles a payment transaction received via the TCP listener.
    """
    logger.info("Handling ISO transaction...")
    
    # Assuming iso_data is already a dictionary for this example
    card_status = _check_card_funds(iso_data.get('card_number'))

    if card_status == 'funded':
        logger.info("Card has sufficient funds. Processing as M1 (onledger) transaction.")
        return handle_onledger_transaction(iso_data)
    else:
        logger.info("Card has insufficient funds. Processing as M0 (offledger) transaction.")
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
    Processes an M0 transaction by initiating an in-house crypto payout.
    """
    logger.info("Processing MO (offledger) transaction...")
    
    # In-house crypto payout
    payout_result = crypto_payouts.make_payout(data.get('payout_type'), data.get('merchant_wallet'), data.get('amount'), data.get('protocol'))
    
    # Save the transaction to the database, including the crypto hash
    database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'offledger', payout_result['status'], payout_result.get('tx_hash'))
    
    return {"status": payout_result['status'], "message": "Payout initiated", "tx_hash": payout_result.get('tx_hash')}
