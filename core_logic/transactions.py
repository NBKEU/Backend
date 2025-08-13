# File: core_logic/transactions.py
# This is the central transaction handler, routing requests based on a card's funding status and payout type.

from . import validation, security, crypto_payouts
from database import database
import time
import logging

logger = logging.getLogger(__name__)

# --- New function to check card's funding status ---
def _check_card_funding_status(card_number):
    """
    Simulates checking the funds loaded on a debit card.
    In a real production system, this would involve a live check with your card issuer or network
    to determine if the transaction can be processed as an online sale.
    """
    # Placeholder logic: for this demo, we'll use the card number length to simulate
    # a check. A real implementation would use a BIN lookup or a live network call.
    sanitized_card_number = card_number.replace(' ', '')
    if len(sanitized_card_number) % 2 == 0:
        return 'online_sale'
    else:
        return 'offline_sale'

# --- New function to handle both onledger and offledger payments/payouts ---
def _process_payment_and_payout(data, transaction_type):
    """
    Processes the payment and, if specified, the crypto payout.
    """
    payout_type = data.get('payout_type')

    if payout_type:
        logger.info(f"Crypto payout requested. Processing as {payout_type}.")
        payout_result = crypto_payouts.make_payout(payout_type, data.get('merchant_wallet'), data.get('amount'), data.get('protocol'))
        database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), transaction_type, payout_result['status'], payout_result.get('tx_hash'))
        return {"status": payout_result['status'], "message": "Payout initiated", "tx_hash": payout_result.get('tx_hash')}
    else:
        logger.info("No crypto payout requested. Processing with external payment gateway.")
        # Placeholder for calling the payment gateway
        # In a real app, this would route the transaction to a traditional payment processor.
        time.sleep(1) # Simulate API call
        result = {"status": "approved", "transaction_id": f"txn_{int(time.time())}"}
        database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), transaction_type, result['status'])
        return result

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
    funding_status = _check_card_funding_status(data.get('card_number'))

    if funding_status == 'online_sale':
        logger.info("Card is funded for online sale.")
        return _process_payment_and_payout(data, 'online_sale')
    else:
        logger.info("Card has insufficient funds. Processing as an offline sale.")
        return _process_payment_and_payout(data, 'offline_sale')


def handle_iso_transaction(iso_data):
    """
    Handles a payment transaction received via the TCP listener.
    """
    logger.info("Handling ISO transaction...")
    
    # Assuming iso_data is already a dictionary for this example
    funding_status = _check_card_funding_status(iso_data.get('card_number'))

    if funding_status == 'online_sale':
        logger.info("Card is funded for online sale.")
        return _process_payment_and_payout(iso_data, 'online_sale')
    else:
        logger.info("Card has insufficient funds. Processing as an offline sale.")
        return _process_payment_and_payout(iso_data, 'offline_sale')
