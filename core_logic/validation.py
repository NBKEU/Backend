import re

def validate_card_number(card_number):
    return re.match(r'^\d{16}$', card_number.replace(' ', '')) is not None

def validate_amount(amount):
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False

def validate_auth_code(auth_code, protocol_name):
    from . import protocol_mapping
    details = protocol_mapping.get_protocol_details(protocol_name)
    if details:
        required_length = details['approval_length']
        return len(auth_code) == required_length
    return False
