from datetime import datetime
from flask import session
from app.extensions import mongo

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