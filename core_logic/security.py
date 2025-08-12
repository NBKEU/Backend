import re

def tokenize_card_data(card_number, expiry, cvv):
    return f"token_{card_number[-4:]}_{expiry.replace('/', '')}"

def detokenize_card_data(token):
    return "DECRYPTED_CARD_DATA"
