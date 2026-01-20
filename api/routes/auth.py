"""
Authentication routes for the API.
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt

from database import create_user, get_user_by_email, get_user_by_id

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    data = request.get_json()
    
    # Validate input
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    name = data.get('name', '').strip()
    
    if not email or not password:
        return jsonify({'error': 'Email dan password wajib diisi'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password minimal 6 karakter'}), 400
    
    # Check if email exists
    existing_user = get_user_by_email(email)
    if existing_user:
        return jsonify({'error': 'Email sudah terdaftar'}), 400
    
    # Hash password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    # Create user
    try:
        user = create_user(email, password_hash, name)
        
        # Generate token
        access_token = create_access_token(identity=str(user['id']))
        
        return jsonify({
            'message': 'Registrasi berhasil',
            'user': {
                'id': user['id'],
                'email': user['email'],
                'name': user['name'],
            },
            'access_token': access_token
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """Login user."""
    data = request.get_json()
    
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    
    if not email or not password:
        return jsonify({'error': 'Email dan password wajib diisi'}), 400
    
    # Get user
    user = get_user_by_email(email)
    if not user:
        return jsonify({'error': 'Email atau password salah'}), 401
    
    # Check password
    if not bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return jsonify({'error': 'Email atau password salah'}), 401
    
    # Generate token
    access_token = create_access_token(identity=str(user['id']))
    
    return jsonify({
        'message': 'Login berhasil',
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
        },
        'access_token': access_token
    })


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_me():
    """Get current user info."""
    user_id = int(get_jwt_identity())
    user = get_user_by_id(user_id)
    
    if not user:
        return jsonify({'error': 'User tidak ditemukan'}), 404
    
    return jsonify({
        'user': {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at'].isoformat() if user['created_at'] else None,
        }
    })
