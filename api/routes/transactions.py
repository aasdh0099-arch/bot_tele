"""
Transaction routes.
"""

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import get_bot_by_id, get_transactions_by_bot

transactions_bp = Blueprint('transactions', __name__, url_prefix='/api')


@transactions_bp.route('/bots/<int:bot_id>/transactions', methods=['GET'])
@jwt_required()
def list_transactions(bot_id: int):
    """List transactions for a bot."""
    user_id = int(get_jwt_identity())
    
    # Verify bot ownership
    bot = get_bot_by_id(bot_id, user_id)
    if not bot:
        return jsonify({'error': 'Bot tidak ditemukan'}), 404
    
    transactions = get_transactions_by_bot(bot_id)
    
    # Calculate stats
    completed = [t for t in transactions if t['status'] == 'completed']
    total_revenue = sum(t['amount'] for t in completed)
    
    return jsonify({
        'transactions': [{
            'id': t['id'],
            'order_id': t['order_id'],
            'product_name': t['product_name'],
            'buyer_username': t['buyer_username'] or t['buyer_name'] or 'Unknown',
            'amount': t['amount'],
            'status': t['status'],
            'payment_method': t['payment_method'],
            'created_at': t['created_at'].isoformat() if t['created_at'] else None,
            'paid_at': t['paid_at'].isoformat() if t['paid_at'] else None,
        } for t in transactions],
        'stats': {
            'total_transactions': len(transactions),
            'completed_transactions': len(completed),
            'total_revenue': total_revenue,
        }
    })
