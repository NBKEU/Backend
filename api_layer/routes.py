from flask import Blueprint, request, jsonify
from core_logic import transactions
from database import database # Import the database module to get history
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/payments/process', methods=['POST'])
def process_payment():
    """
    Handles a payment request from the web virtual terminal.
    """
    try:
        request_data = request.get_json()
        logger.info(f"Received new payment request from API: {request_data}")
        
        # Pass the request data to the core transaction logic
        result = transactions.handle_http_transaction(request_data)

        if result['status'] == 'approved' or result['status'] == 'success':
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        logger.error(f"Error processing API payment: {e}")
        return jsonify({'status': 'error', 'message': 'Internal Server Error'}), 500
        
@api_bp.route('/history', methods=['GET'])
def get_history():
    """
    Retrieves the transaction history from the database.
    """
    history = database.get_transaction_history()
    return jsonify(history), 200
