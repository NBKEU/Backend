# File: core_logic/protocol_mapping.py
# This module provides functions to access the defined protocols.

from config import Config

PROTOCOLS = Config.PROTOCOLS

def get_protocol_details(protocol_name):
    """Retrieves details for a given protocol name."""
    return PROTOCOLS.get(protocol_name)

def is_onledger_transaction(protocol_name):
    """Checks if a protocol requires on-ledger processing."""
    details = get_protocol_details(protocol_name)
    return details['is_onledger'] if details else False
