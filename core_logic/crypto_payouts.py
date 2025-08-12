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

def _send_rpc_request(url, method, params):
    headers = {'Content-Type': 'application/json'}
    payload = {"jsonrpc": "2.0", "method": method, "params": params, "id": 1}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed to {url}: {e}")
        return {"error": {"message": str(e)}}

def payout_erc20(to_address, amount):
    try:
        w3 = Web3(HTTPProvider(Config.INFURA_API_URL))
        if not w3.is_connected():
            return {"status": "error", "message": "Failed to connect to Ethereum network."}

        erc20_abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"remaining","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_from","type":"address"},{"indexed":true,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"_owner","type":"address"},{"indexed":true,"name":"_spender","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Approval","type":"event"}]')
        
        usdt_contract = w3.eth.contract(address=w3.to_checksum_address(Config.ERC20_TOKEN_CONTRACT_ADDRESS), abi=erc20_abi)
        
        tx = usdt_contract.functions.transfer(
            to_address,
            int(float(amount) * 10**6)
        ).build_transaction({
            'from': Config.CRYPTO_SENDER_WALLET_ADDRESS,
            'nonce': w3.eth.get_transaction_count(Config.CRYPTO_SENDER_WALLET_ADDRESS),
            'gas': 100000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 1,
        })
        
        signed_tx = w3.eth.account.sign_transaction(tx, private_key=Config.CRYPTO_SENDER_PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        
        logger.info(f"ERC-20 payout successful, transaction hash: {w3.to_hex(tx_hash)}")
        return {"status": "success", "tx_hash": w3.to_hex(tx_hash)}

    except Exception as e:
        logger.error(f"Failed to process ERC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

def payout_trc20(to_address, amount):
    try:
        from tronpy import Tron
        from tronpy.keys import PrivateKey
        
        client = Tron(network='mainnet', api_key=Config.TRONGRID_API_KEY)
        client.timeout = 30
        
        pri_key = PrivateKey(bytes.fromhex(Config.CRYPTO_SENDER_PRIVATE_KEY))
        usdt_contract = client.get_contract(Config.TRC20_TOKEN_CONTRACT_ADDRESS)
        
        txn = usdt_contract.functions.transfer(to_address, int(float(amount) * 10**6))
        tx_id = txn.build().sign(pri_key).broadcast()
        
        logger.info(f"TRC-20 payout successful, transaction hash: {tx_id}")
        return {"status": "success", "tx_hash": tx_id}
    
    except Exception as e:
        logger.error(f"Failed to process TRC-20 payout: {e}")
        return {"status": "error", "message": str(e)}

def make_payout(payout_type, to_address, amount, protocol_name):
    logger.info(f"Attempting to make {payout_type} payout for protocol {protocol_name}")
    if payout_type.upper() == "USDT-ERC-20":
        return payout_erc20(to_address, amount)
    elif payout_type.upper() == "USDT-TRC-20":
        return payout_trc20(to_address, amount)
    else:
        return {"status": "error", "message": "Unsupported payout type"}

