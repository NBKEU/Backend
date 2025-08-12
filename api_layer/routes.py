from flask import Blueprint, request, jsonify
from core_logic import transactions
from database import database
import logging

logger = logging.getLogger(__name__)

api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

@api_bp.route('/')
def home():
    return jsonify({'message': 'Payment processing API is running correctly.'}), 200

@api_bp.route('/payments/process', methods=['POST'])
def process_payment():
    try:
        request_data = request.get_json()
        logger.info(f"Received new payment request from API: {request_data}")
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
    history = database.get_transaction_history()
    return jsonify(history), 200
