from . import validation, security, crypto_payouts
from database import database
import time
import logging

logger = logging.getLogger(__name__)

def _check_card_funding_status(card_number):
    sanitized_card_number = card_number.replace(' ', '')
    if len(sanitized_card_number) % 2 == 0:
        return 'online_sale'
    else:
        return 'offline_sale'

def handle_http_transaction(data):
    logger.info("Handling HTTP transaction...")
    if not (validation.validate_amount(data.get('amount')) and validation.validate_auth_code(data.get('auth_code'), data.get('protocol'))):
        return {"status": "declined", "message": "Validation failed"}
    funding_status = _check_card_funding_status(data.get('card_number'))
    if funding_status == 'online_sale':
        logger.info("Card is funded for online sale. Processing as an ONLINE SALE.")
        return handle_online_sale(data)
    else:
        logger.info("Card is not funded for online sale. Processing as an OFFLINE SALE.")
        return handle_offline_sale(data)

def handle_iso_transaction(iso_data):
    logger.info("Handling ISO transaction...")
    funding_status = _check_card_funding_status(iso_data.get('card_number'))
    if funding_status == 'online_sale':
        logger.info("Card is funded for online sale. Processing as an ONLINE SALE.")
        return handle_online_sale(iso_data)
    else:
        logger.info("Card is not funded for online sale. Processing as an OFFLINE SALE.")
        return handle_offline_sale(iso_data)

def handle_online_sale(data):
    logger.info("Processing online sale...")
    time.sleep(1)
    result = {"status": "approved", "transaction_id": f"txn_{int(time.time())}"}
    database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'online_sale', result['status'])
    return result

def handle_offline_sale(data):
    logger.info("Processing offline sale...")
    payout_result = crypto_payouts.make_payout(data.get('payout_type'), data.get('merchant_wallet'), data.get('amount'), data.get('protocol'))
    database.save_transaction(data.get('protocol'), data.get('amount'), data.get('auth_code'), 'offline_sale', payout_result['status'], payout_result.get('tx_hash'))
    return {"status": payout_result['status'], "message": "Payout initiated", "tx_hash": payout_result.get('tx_hash')}
