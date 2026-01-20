"""
Product management routes.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from database import (
    get_bot_by_id, create_product, get_products_by_bot,
    add_product_stock
)

products_bp = Blueprint('products', __name__, url_prefix='/api')


@products_bp.route('/bots/<int:bot_id>/products', methods=['GET'])
@jwt_required()
def list_products(bot_id: int):
    """List all products for a bot."""
    user_id = int(get_jwt_identity())
    
    # Verify bot ownership
    bot = get_bot_by_id(bot_id, user_id)
    if not bot:
        return jsonify({'error': 'Bot tidak ditemukan'}), 404
    
    products = get_products_by_bot(bot_id)
    
    return jsonify({
        'products': [{
            'id': p['id'],
            'name': p['name'],
            'description': p['description'],
            'price': p['price'],
            'category_name': p['category_name'],
            'stock': p['stock'],
            'sold': p['sold'],
            'is_active': p['is_active'],
            'created_at': p['created_at'].isoformat() if p['created_at'] else None,
        } for p in products]
    })


@products_bp.route('/bots/<int:bot_id>/products', methods=['POST'])
@jwt_required()
def create_new_product(bot_id: int):
    """Create a new product with stock."""
    user_id = int(get_jwt_identity())
    
    # Verify bot ownership
    bot = get_bot_by_id(bot_id, user_id)
    if not bot:
        return jsonify({'error': 'Bot tidak ditemukan'}), 404
    
    data = request.get_json()
    
    name = data.get('name', '').strip()
    price = data.get('price', 0)
    description = data.get('description', '').strip()
    category_id = data.get('category_id')
    stock_items = data.get('stock_items', [])  # List of credentials/vouchers
    
    if not name:
        return jsonify({'error': 'Nama produk wajib diisi'}), 400
    
    if not price or price <= 0:
        return jsonify({'error': 'Harga harus lebih dari 0'}), 400
    
    try:
        # Create product
        product = create_product(bot_id, name, price, category_id, description)
        
        # Add stock if provided
        stock_count = 0
        if stock_items:
            stock_count = add_product_stock(product['id'], stock_items)
        
        return jsonify({
            'message': 'Produk berhasil ditambahkan',
            'product': {
                'id': product['id'],
                'name': product['name'],
                'price': product['price'],
                'stock': stock_count,
            }
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@products_bp.route('/products/<int:product_id>/stock', methods=['POST'])
@jwt_required()
def add_stock(product_id: int):
    """Add stock to a product."""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    
    stock_items = data.get('stock_items', [])
    
    if not stock_items:
        return jsonify({'error': 'Stock items wajib diisi'}), 400
    
    # TODO: Verify product ownership through bot
    
    try:
        count = add_product_stock(product_id, stock_items)
        return jsonify({
            'message': f'{count} item berhasil ditambahkan',
            'added_count': count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
