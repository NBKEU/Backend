# File: main.py
# This is the main entry point for your production-grade payment processing backend.
# It initializes and runs both the TCP listener and the Flask web API concurrently.

import threading
import socket
import logging
from flask import Flask
from werkzeug.serving import make_server
import time

from config import Config
from api_layer.routes import api_bp
from core_logic import transactions, protocol_mapping

# --- Logging Setup ---
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('main_app')

# --- TCP Server for Android Terminals ---
class TCPServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.is_running = True

    def run(self):
        self.server_socket.listen(5)
        logger.info(f"TCP Listener started on {self.host}:{self.port}")
        while self.is_running:
            try:
                conn, addr = self.server_socket.accept()
                logger.info(f"Accepted TCP connection from {addr}")
                client_handler = threading.Thread(target=self.handle_client, args=(conn,))
                client_handler.start()
            except socket.error as e:
                if self.is_running:
                    logger.error(f"TCP accept error: {e}")
                break

  def handle_client(self, conn):  # FIX: Add 'conn' to the method signature
        try:
            while True:
                # Receive data from the terminal (ISO 8583 message)
                data = conn.recv(1024)
                if not data:
                    break
                    
                logger.info(f"Received raw data from TCP: {data.decode()}")
                
                # Placeholder for ISO 8583 parsing
                iso_message = {
                    'protocol': 'POS Terminal -101.8 (PIN-LESS transaction)',
                    'amount': '50.00',
                    'auth_code': '4567',
                    'payout_type': 'USDT-ERC-20',
                    'merchant_wallet': '0x73F888dcE062d2acD4A7688386F0f92f43055491'
                }

                # Call the core business logic
                response = transactions.handle_iso_transaction(iso_message)
                    
                # Placeholder for packing the response back into ISO 8583
                response_iso_message = f"ISO RESPONSE: {response['status']}"
                conn.sendall(response_iso_message.encode('utf-8'))

        except Exception as e:
            logger.error(f"Error handling client connection: {e}")
        finally:
            conn.close()
            logger.info("TCP connection closed.")
            
    def stop(self):
        self.is_running = False
        dummy_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dummy_sock.connect((self.host, self.port))
        dummy_sock.close()
        self.server_socket.close()

# --- Flask Web Server for Virtual Terminals ---
class FlaskServer(threading.Thread):
    def __init__(self, host, port):
        super().__init__()
        self.app = Flask(__name__)
        self.app.register_blueprint(api_bp)
        self.srv = make_server(host, port, self.app)
        self.ctx = self.app.app_context()
        self.ctx.push()

    def run(self):
        logger.info(f"Flask Web Server started on http://{self.srv.host}:{self.srv.port}")
        self.srv.serve_forever()

    def stop(self):
        self.srv.shutdown()

# --- Main Application Logic ---
def main():
    logger.info("Starting payment processing backend...")
    
    tcp_server = TCPServer(Config.TCP_HOST, Config.TCP_PORT)
    tcp_server.start()

    flask_server = FlaskServer(Config.WEB_HOST, Config.WEB_PORT)
    flask_server.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down servers...")
        flask_server.stop()
        tcp_server.stop()
        flask_server.join()
        tcp_server.join()
        logger.info("Servers shut down successfully.")

if __name__ == "__main__":
    main()
