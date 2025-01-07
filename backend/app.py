# app.py
from flask import Flask, request, jsonify, session
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import os
from functools import wraps

app = Flask(__name__)
CORS(app, supports_credentials=True)
bcrypt = Bcrypt(app)

# Configuration
app.config['MONGO_URI'] = 'mongodb://localhost:27017/squid'
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

mongo = PyMongo(app)

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Authentication routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if mongo.db.users.find_one({'email': data['email']}):
        return jsonify({'error': 'Email already exists'}), 400
    
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = {
        'email': data['email'],
        'password': hashed_password,
        'preferences': {
            'theme': 'light',
            'notifications': 'enabled',
            'language': 'English'
        },
        'created_at': datetime.utcnow()
    }
    
    mongo.db.users.insert_one(user)
    return jsonify({'message': 'User registered successfully'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = mongo.db.users.find_one({'email': data['email']})
    
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        session['user_id'] = str(user['_id'])
        session.permanent = True
        
        # Initialize session data
        session['start_time'] = datetime.utcnow().isoformat()
        session['pages_visited'] = []
        
        return jsonify({
            'message': 'Login successful',
            'preferences': user.get('preferences', {})
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'}), 200

# Preferences routes
@app.route('/api/preferences', methods=['POST'])
@login_required
def update_preferences():
    data = request.get_json()
    mongo.db.users.update_one(
        {'_id': session['user_id']},
        {'$set': {'preferences': data}}
    )
    
    # Log preference update activity
    log_activity('update_preferences', {
        'new_preferences': data
    })
    
    return jsonify({'message': 'Preferences updated successfully'})

# Session routes
@app.route('/api/session/page', methods=['POST'])
@login_required
def log_page_visit():
    data = request.get_json()
    page = data.get('page')
    
    if not page:
        return jsonify({'error': 'Page name is required'}), 400
    
    if 'pages_visited' not in session:
        session['pages_visited'] = []
    
    visit = {
        'page': page,
        'timestamp': datetime.utcnow().isoformat()
    }
    session['pages_visited'].append(visit)
    
    # Log the page visit as an activity
    log_activity('page_visit', {'page': page})
    
    return jsonify({'message': 'Page visit logged'})

@app.route('/api/session', methods=['GET'])
@login_required
def get_session_info():
    if 'start_time' not in session:
        return jsonify({'error': 'No active session'}), 404
    
    # Pagination parameters
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Get all pages visited in current session
    pages_visited = session.get('pages_visited', [])
    
    # Calculate pagination
    total_pages = len(pages_visited)
    total_pages_count = (total_pages + per_page - 1) // per_page
    
    # Slice the pages based on pagination
    start_idx = (page - 1) * per_page
    end_idx = start_idx + per_page
    paginated_pages = pages_visited[start_idx:end_idx]
    
    duration = (datetime.utcnow() - datetime.fromisoformat(session['start_time'])).seconds
    
    return jsonify({
        'start_time': session['start_time'],
        'duration_seconds': duration,
        'pages_visited': paginated_pages,
        'pagination': {
            'current_page': page,
            'per_page': per_page,
            'total_pages': total_pages_count,
            'total_items': total_pages
        }
    })

@app.route('/api/activities', methods=['GET'])
@login_required
def get_activities():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    # Get total count
    total_activities = mongo.db.activities.count_documents({
        'user_id': session['user_id']
    })
    
    # Get paginated activities
    activities = mongo.db.activities.find(
        {'user_id': session['user_id']},
        {'_id': 0}  # Exclude MongoDB ID
    ).sort('timestamp', -1).skip((page - 1) * per_page).limit(per_page)
    
    return jsonify({
        'activities': list(activities),
        'pagination': {
            'current_page': page,
            'per_page': per_page,
            'total_pages': (total_activities + per_page - 1) // per_page,
            'total_items': total_activities
        }
    })


def log_activity(action, details=None):
    if not details:
        details = {}
    
    activity = {
        'user_id': session.get('user_id'),
        'session_id': session.get('session_id'),
        'action': action,
        'details': details,
        'timestamp': datetime.utcnow()
    }
    
    mongo.db.activities.insert_one(activity)


if __name__ == '__main__':
    app.run(debug=True)