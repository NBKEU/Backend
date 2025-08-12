from config import Config

PROTOCOLS = Config.PROTOCOLS

def get_protocol_details(protocol_name):
    return PROTOCOLS.get(protocol_name)

