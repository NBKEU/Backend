# File: main.py
# This is the corrected main entry point for your production-grade Flask backend.
# It is designed to be run by Gunicorn. The TCP listener should be a separate service.

import threading
import socket
import logging
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
import time
from starkbank_iso8583 import parser

# To fix the ModuleNotFoundError on Render
sys.path.insert(0, '/opt/render/project/src/.venv/lib/python3.13/site-packages')

from api_layer.routes import api_bp
from core_logic import transactions, protocol_mapping
from config import Config

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_app')

# --- Create the Flask App Object ---
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.register_blueprint(api_bp)

@app.route('/')
def home():
    return jsonify({'message': 'Payment processing API is running correctly.'}), 200

# --- TCP Listener for Android Terminals ---
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
            data = conn.recv(1024)
            if data:
                try:
                    iso_message = parser.unpack(data.decode('utf-8'))
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
    tcp_thread = threading.Thread(target=run_tcp_server)
    tcp_thread.daemon = True
    tcp_thread.start()
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 5000), debug=True)
