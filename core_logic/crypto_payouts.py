# File: core_logic/crypto_payouts.py
# This module handles the secure API calls for cryptocurrency payouts using
# Infura/Alchemy for ERC-20 and TronGrid for TRC-20.

import requests
import json
import logging
from config import Config

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
def _create_erc20_transaction(to_address, amount_in_wei):
    """
    Builds and signs an Ethereum transaction for an ERC-20 token.
    This is a conceptual placeholder for a complex process.
    """
    # In a real implementation, you would:
    # 1. Use a library like `web3.py` to connect to Infura/Alchemy.
    # 2. Get the current nonce and gas price.
    # 3. Build the raw transaction.
    # 4. Sign the transaction with your private key.
    # This is a critical security-sensitive area.
    logger.info(f"Creating ERC-20 transaction to {to_address} for {amount_in_wei} wei")
    
    # Placeholder response for a signed transaction
    signed_tx = "0xSignedTransactionHex"
    return signed_tx

def payout_erc20(to_address, amount):
    """
    Initiates an ERC-20 crypto payout via Infura or Alchemy.
    """
    # We will use Infura for this example, but you can switch to Alchemy easily.
    api_url = Config.INFURA_API_URL
    
    # Convert amount to wei (e.g., 1 ETH = 10^18 wei)
    amount_in_wei = int(float(amount) * 10**18)
    
    # The actual process involves a series of API calls.
    try:
        # Step 1: Create and sign the transaction (placeholder)
        signed_tx = _create_erc20_transaction(to_address, amount_in_wei)
        
        # Step 2: Broadcast the signed transaction to the network
        logger.info(f"Broadcasting ERC-20 transaction via Infura...")
        response = _send_rpc_request(api_url, "eth_sendRawTransaction", [signed_tx])
        
        if "result" in response:
            tx_hash = response["result"]
            logger.info(f"ERC-20 payout successful, transaction hash: {tx_hash}")
            return {"status": "success", "tx_hash": tx_hash}
        else:
            logger.error(f"ERC-20 payout failed: {response.get('error', {})}")
            return {"status": "error", "message": response.get('error', {}).get('message', 'Unknown error')}
            
    except Exception as e:
        logger.error(f"Failed to process ERC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

# --- TRC-20 Payouts (TronGrid) ---
def _create_trc20_transaction(to_address, amount):
    """
    Builds and signs a TRON transaction for a TRC-20 token.
    This is a conceptual placeholder for a complex process.
    """
    # In a real implementation, you would use a Tron library.
    logger.info(f"Creating TRC-20 transaction to {to_address} for {amount}")
    
    # Placeholder response for a signed transaction
    signed_tx = "TRON_SignedTransactionHex"
    return signed_tx

def payout_trc20(to_address, amount):
    """
    Initiates a TRC-20 crypto payout via TronGrid.
    """
    api_url = Config.TRONGRID_API_URL
    
    try:
        # Step 1: Create and sign the transaction (placeholder)
        signed_tx = _create_trc20_transaction(to_address, amount)
        
        # Step 2: Broadcast the signed transaction
        logger.info(f"Broadcasting TRC-20 transaction via TronGrid...")
        response = _send_rpc_request(f"{api_url}/wallet/broadcasttransaction", "broadcasttransaction", [signed_tx])
        
        if response.get("result"): # TronGrid returns {"result": true} for success
            tx_hash = response.get("txid")
            logger.info(f"TRC-20 payout successful, transaction hash: {tx_hash}")
            return {"status": "success", "tx_hash": tx_hash}
        else:
            logger.error(f"TRC-20 payout failed: {response.get('error', {})}")
            return {"status": "error", "message": response.get('message', 'Unknown error')}
            
    except Exception as e:
        logger.error(f"Failed to process TRC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

def make_payout(payout_type, to_address, amount, protocol_name):
    """
    Central function to route the payout to the correct blockchain service.
    """
    logger.info(f"Attempting to make {payout_type} payout for protocol {protocol_name}")
    if payout_type.upper() == "ERC-20":
        return payout_erc20(to_address, amount)
    elif payout_type.upper() == "TRC-20":
        return payout_trc20(to_address, amount)
    else:
        return {"status": "error", "message": "Unsupported payout type"}
