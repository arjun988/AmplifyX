from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app.models.user import User
from app.extensions import bcrypt
from app.utils.logger import log_activity

bp = Blueprint('auth', __name__, url_prefix='/api')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.get_by_email(data['email']):
        return jsonify({'error': 'Email already exists'}), 400
    
    User.create(data['email'], data['password'])
    return jsonify({'message': 'User registered successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.get_by_email(data['email'])
    
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        session['user_id'] = str(user['_id'])
        session.permanent = True
        session['start_time'] = datetime.utcnow().isoformat()
        session['pages_visited'] = []
        
        return jsonify({
            'message': 'Login successful',
            'preferences': user.get('preferences', {})
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200