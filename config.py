import os

class Config:
    # TCP Listener settings for Android terminals
    TCP_HOST = os.environ.get('TCP_HOST', '0.0.0.0')
    TCP_PORT = int(os.environ.get('TCP_PORT', 9000))

    # Flask Web API settings for virtual terminals
    WEB_HOST = os.environ.get('WEB_HOST', '0.0.0.0')
    WEB_PORT = int(os.environ.get('PORT', 5000))

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
    INFURA_API_KEY = os.environ.get('INFURA_API_KEY', "YOUR_INFURA_API_KEY")
    INFURA_API_URL = f"https://mainnet.infura.io/v3/{INFURA_API_KEY}"
    TRONGRID_API_KEY = os.environ.get('TRONGRID_API_KEY', "YOUR_TRONGRID_API_KEY")
    TRONGRID_API_URL = "https://api.trongrid.io"

    # Wallet credentials for payouts (sender's wallet)
    CRYPTO_SENDER_WALLET_ADDRESS = os.environ.get('CRYPTO_SENDER_WALLET_ADDRESS', "0xYourSenderWalletAddressHere")
    CRYPTO_SENDER_PRIVATE_KEY = os.environ.get('CRYPTO_SENDER_PRIVATE_KEY', "YourSenderCryptoPrivateKeyHere")

    # --- TOKEN CONTRACTS ---
    ERC20_TOKEN_CONTRACT_ADDRESS = os.environ.get('ERC20_TOKEN_CONTRACT_ADDRESS', "0xdAC17F958D2ee523a2206206994597C13D831ec7")
    TRC20_TOKEN_CONTRACT_ADDRESS = os.environ.get('TRC20_TOKEN_CONTRACT_ADDRESS', "TR7NHqjeFpX9yB1Jg1a5X6eR5yvUfR7T")

    # --- DATABASE SETTINGS ---
    DB_NAME = os.environ.get('DB_NAME', 'your_db_name')
    DB_USER = os.environ.get('DB_USER', 'your_db_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'your_db_password')
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_PORT = os.environ.get('DB_PORT', '5432')
