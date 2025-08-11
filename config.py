# File: config.py
# This file stores all configuration settings for the application.
# Using a separate file for config makes it easy to manage different
# settings for development, testing, and production environments.

class Config:
    # TCP Listener settings for Android terminals
    TCP_HOST = '0.0.0.0'
    TCP_PORT = 9000

    # Flask Web API settings for virtual terminals
    WEB_HOST = '0.0.0.0'
    WEB_PORT = 5000

    # Your custom POS terminal protocols mapping
    PROTOCOLS = {
        "POS Terminal -101.1 (4-digit approval)": {"approval_length": 4, "is_onledger": True},
        "POS Terminal -101.4 (6-digit approval)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -101.6 (Pre-authorization)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -101.7 (4-digit approval)": {"approval_length": 4, "is_onledger": True},
        "POS Terminal -101.8 (PIN-LESS transaction)": {"approval_length": 4, "is_onledger": False}, # Example MO transaction
        "POS Terminal -201.1 (6-digit approval)": {"approval_length": 6, "is_onledger": True},
        "POS Terminal -201.3 (6-digit approval)": {"approval_length": 6, "is_onledger": False}, # Example MO transaction
        "POS Terminal -201.5 (6-digit approval)": {"approval_length": 6, "is_onledger": False}  # Example MO transaction
    }

    # --- CRYPTOCURRENCY PAYOUT SETTINGS ---
    # API keys and endpoints for blockchain providers
    INFURA_API_KEY = "6aaea4c2d2be42bf89c660d07863fea5"
    INFURA_API_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"

    INFURA_API_KEY = "6aaea4c2d2be42bf89c660d07863fea5"
    INFURA_API_URL = f"https://mainnet.infura.io/v3/6aaea4c2d2be42bf89c660d07863fea5{INFURA_API_URL}"

    TRONGRID_API_URL = "https://api.trongrid.io"

    # Wallet credentials for payouts (sender's wallet)
    CRYPTO_SENDER_WALLET_ADDRESS = "0xYourSenderWalletAddressHere"
    CRYPTO_SENDER_PRIVATE_KEY = "YourSenderCryptoPrivateKeyHere"
    
    # Placeholder for Payment Gateway API credentials
    PAYMENT_GATEWAY_API_KEY = "YourPaymentGatewayApiKey"
