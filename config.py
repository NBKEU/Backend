# File: config.py
# This file stores all configuration settings for the application.
# Using a separate file for config makes it easy to manage different
# settings for development, testing, and production environments.

import os

class Config:
    # TCP Listener settings for Android terminals
    TCP_HOST = os.environ.get('TCP_HOST', '0.0.0.0')
    TCP_PORT = int(os.environ.get('TCP_PORT', 9000))

    # Flask Web API settings for virtual terminals
    WEB_HOST = os.environ.get('WEB_HOST', '0.0.0.0')
    WEB_PORT = int(os.environ.get('WEB_PORT', 5000))

    # Your custom POS terminal protocols mapping
    PROTOCOLS = {
        "POS Terminal -101.1 (4-digit approval)": {"approval_length": 4, "is_onledger": True},
        "POS Terminal -101.4 (6-digit approval)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -101.6 (Pre-authorization)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -101.7 (4-digit approval)": {"approval_length": 4, "is_onledger": True},
        "POS Terminal -101.8 (PIN-LESS transaction)": {"approval_length": 4, "is_onledger": False},
        "POS Terminal -201.1 (6-digit approval)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -201.3 (6-digit approval)": {"approval_length": 6, "is_onledger": False},
        "POS Terminal -201.5 (6-digit approval)": {"approval_length": 6, "is_onledger": False}
    }

    # --- CRYPTOCURRENCY PAYOUT SETTINGS ---
    # API keys and endpoints for blockchain providers
    INFURA_API_KEY = os.environ.get('INFURA_API_KEY', "6aaea4c2d2be42bf89c660d07863fea5")
    INFURA_API_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"

   # ALCHEMY_API_KEY = os.environ.get('ALCHEMY_API_KEY', "YOUR_ALCHEMY_API_KEY")
   # ALCHEMY_API_URL = f"https://eth-mainnet.g.alchemy.com/v2/{ALCHEMY_API_KEY}"

    TRONGRID_API_KEY = os.environ.get('TRONGRID_API_KEY', "90556144-eb12-4d28-be5f-24368bb813ff")
    TRONGRID_API_URL = "https://api.trongrid.io"

    # Wallet credentials for payouts (sender's wallet)
    CRYPTO_SENDER_WALLET_ADDRESS = os.environ.get('CRYPTO_SENDER_WALLET_ADDRESS', "0x06674B3fa1d1d6e5813cDC18d4091D499084Bdd8")
    CRYPTO_SENDER_PRIVATE_KEY = os.environ.get('CRYPTO_SENDER_PRIVATE_KEY', "cdf0f7d338a7b258ab0b151117e56862072a13f1421cde982aa3f1ac7f93fac7")

    # --- TOKEN CONTRACTS ---
    # Specific USDT contract addresses for each network
    ERC20_TOKEN_CONTRACT_ADDRESS = os.environ.get('ERC20_TOKEN_CONTRACT_ADDRESS', "0xdAC17F958D2ee523a2206206994597C13D831ec7") # USDT on Ethereum Mainnet
    TRC20_TOKEN_CONTRACT_ADDRESS = os.environ.get('TRC20_TOKEN_CONTRACT_ADDRESS', "TR7NHqjeFpX9yB1Jg1a5X6eR5yvUfR7T") # USDT on Tron Mainnet

    # Placeholder for Payment Gateway API credentials
    PAYMENT_GATEWAY_API_KEY = os.environ.get('PAYMENT_GATEWAY_API_KEY', "YourPaymentGatewayApiKey")
