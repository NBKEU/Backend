# File: core_logic/validation.py
# This module contains all data validation functions.

import re

def validate_card_number(card_number):
    """A simple Luhn algorithm validation (placeholder)."""
    # In a production app, this would be more robust.
    return re.match(r'^\d{16}$', card_number.replace(' ', '')) is not None

def validate_amount(amount):
    """Validates that the amount is a positive number."""
    try:
        return float(amount) > 0
    except (ValueError, TypeError):
        return False

def validate_auth_code(auth_code, protocol_name):
    """Validates the length of the authorization code based on the protocol."""
    from . import protocol_mapping
    details = protocol_mapping.get_protocol_details(protocol_name)
    if details:
        required_length = details['approval_length']
        return len(auth_code) == required_length
    return False
