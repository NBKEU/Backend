# File: core_logic/crypto_payouts.py
# This module handles the secure API calls for cryptocurrency payouts using
# Infura/Alchemy for ERC-20 and TronGrid for TRC-20.

import os
import requests
import json
import logging
from config import Config
from web3 import Web3, HTTPProvider
# You would also import Tronpy here if you were using it
# from tronpy import Tron
# from tronpy.keys import PrivateKey

logger = logging.getLogger(__name__)

# --- Common helper function for making API requests ---
def _send_rpc_request(url, method, params):
    """
    Sends a generic JSON-RPC request to a blockchain API endpoint.
    """
    headers = {'Content-Type': 'application/json'}
    payload = {
        "jsonrpc": "2.0",
        "method": method,
        "params": params,
        "id": 1
    }
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed to {url}: {e}")
        return {"error": {"message": str(e)}}

# --- ERC-20 Payouts (Infura/Alchemy) ---
def _create_and_broadcast_erc20_transaction(to_address, amount_in_wei):
    """
    Builds, signs, and broadcasts an Ethereum transaction for an ERC-20 token.
    """
    try:
        # Use a Web3 provider to connect to Infura/Alchemy
        w3 = Web3(HTTPProvider(Config.INFURA_API_URL))
        if not w3.is_connected():
            return {"status": "error", "message": "Failed to connect to Ethereum network."}

        # --- IMPORTANT: Placeholder for real token contract logic ---
        # You would need the contract address and ABI for USDT
        # For a real implementation, you would need to initialize the contract here.
        # token_contract = w3.eth.contract(address=token_address, abi=token_abi)
        
        # --- Transaction details ---
        nonce = w3.eth.get_transaction_count(Config.CRYPTO_SENDER_WALLET_ADDRESS)
        gas_price = w3.eth.gas_price

        # --- Build transaction (placeholder) ---
        # This is a mock transaction that would need to be replaced.
        tx = {
            'nonce': nonce,
            'from': Config.CRYPTO_SENDER_WALLET_ADDRESS,
            'to': to_address,
            'value': amount_in_wei,
            'gas': 200000, # This should be estimated correctly
            'gasPrice': gas_price,
            'chainId': 1, # Mainnet chain ID
        }
        
        # --- Sign the transaction with your private key ---
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=Config.CRYPTO_SENDER_PRIVATE_KEY)

        # --- Broadcast the signed transaction ---
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logger.info(f"ERC-20 payout successful, transaction hash: {w3.to_hex(tx_hash)}")
        return {"status": "success", "tx_hash": w3.to_hex(tx_hash)}

    except Exception as e:
        logger.error(f"Failed to process ERC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

def payout_erc20(to_address, amount):
    """
    Initiates an ERC-20 crypto payout via Infura or Alchemy.
    """
    amount_in_wei = int(float(amount) * 10**18)
    return _create_and_broadcast_erc20_transaction(to_address, amount_in_wei)


# --- TRC-20 Payouts (TronGrid) ---
def payout_trc20(to_address, amount):
    """
    Initiates a TRC-20 crypto payout via TronGrid.
    """
    try:
        # --- IMPORTANT: Placeholder for real Tronpy logic ---
        # This would require a Tronpy client and the correct contract details.
        # from tronpy import Tron
        # tron = Tron(network='mainnet', api_key=Config.TRONGRID_API_KEY)
        
        # --- Build, sign, and broadcast transaction (placeholder) ---
        # This is a mock process
        logger.info(f"Creating TRC-20 transaction to {to_address} for {amount} USDT")
        # Placeholder transaction hash
        tx_hash = "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2"
        
        return {"status": "success", "tx_hash": tx_hash}
    except Exception as e:
        logger.error(f"Failed to process TRC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

def make_payout(payout_type, to_address, amount, protocol_name):
    """
    Central function to route the payout to the correct blockchain service.
    """
    logger.info(f"Attempting to make {payout_type} payout for protocol {protocol_name}")
    if payout_type.upper() == "USDT-ERC-20":
        return payout_erc20(to_address, amount)
    elif payout_type.upper() == "USDT-TRC-20":
        return payout_trc20(to_address, amount)
    else:
        return {"status": "error", "message": "Unsupported payout type"}
