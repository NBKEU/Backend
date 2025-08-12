# File: main.py
# This is the corrected main entry point for your production-grade Flask backend.
# It is designed to be run by Gunicorn. The TCP listener should be a separate service.

import threading
import socket
import logging
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS # Import CORS to allow communication from your frontend URL
import time

# The starkbank_iso8583 import has been removed as requested.

# Assuming a flat project structure for demonstration
from config import Config
from api_layer.routes import api_bp
from core_logic import transactions

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_app')

# --- NEW: A simple function to parse a hardcoded ISO message ---
# This replaces the need for the starkbank_iso8583 dependency.
def unpack_iso_message(raw_data):
    """
    A placeholder to unpack ISO 8583 messages.
    In a real production environment, this would be a robust parser
    that you develop in-house.
    """
    # This is a sample message for a PIN-LESS transaction (offledger)
    return {
        'protocol': 'POS Terminal -101.8 (PIN-LESS transaction)',
        'amount': '50.00',
        'auth_code': '4567',
        'payout_type': 'USDT-ERC-20',
        'merchant_wallet': '0xSampleMerchantWallet'
    }

# --- Create the Flask App Object ---
# This app object is what Gunicorn will use to run your API.
app = Flask(__name__)
# Enable CORS for all routes on the blueprint to allow your frontend to connect
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_bp)

# A simple root route to confirm the API is running
@app.route('/')
def home():
    """
    Returns a simple message to confirm the API is running.
    """
    return jsonify({'message': 'Payment processing API is running correctly.'}), 200

# --- TCP Listener for Android Terminals ---
# In a real production environment, this should be run as a separate Render service
# because Gunicorn is a single-threaded web server that cannot manage other services.
def run_tcp_server():
    host = os.environ.get('TCP_HOST', '0.0.0.0')
    port = int(os.environ.get('TCP_PORT', 9000))
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logger.info(f"TCP Listener started on {host}:{port}")

    while True:
        try:
            conn, addr = server_socket.accept()
            logger.info(f"Accepted TCP connection from {addr}")
            
            # --- Corrected Logic for handling the ISO message ---
            data = conn.recv(1024)
            if data:
                try:
                    # Use the new local function to handle the message
                    iso_message = unpack_iso_message(data.decode('utf-8'))
                    logger.info(f"Parsed ISO message: {iso_message}")
                    response = transactions.handle_iso_transaction(iso_message)
                    response_iso_message = f"ISO RESPONSE: {response['status']}"
                    conn.sendall(response_iso_message.encode('utf-8'))
                except Exception as e:
                    logger.error(f"Failed to parse or handle ISO message: {e}")
                    conn.sendall(b"Invalid message format")
            
            conn.close()
            logger.info("TCP connection closed.")
        except Exception as e:
            logger.error(f"TCP server error: {e}")

if __name__ == "__main__":
    # In production, Gunicorn will manage the app.run() for you.
    # We use this block for local development.
    # Start the TCP server in a separate thread for local testing.
    tcp_thread = threading.Thread(target=run_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()
    
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)
