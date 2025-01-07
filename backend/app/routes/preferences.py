from flask import Blueprint, request, jsonify, session
from app.utils.decorators import login_required
from app.utils.logger import log_activity
from app.extensions import mongo

bp = Blueprint('preferences', __name__, url_prefix='/api')

@bp.route('/preferences', methods=['POST'])
@login_required
def update_preferences():
    data = request.get_json()
    mongo.db.users.update_one(
        {'_id': session['user_id']},
        {'$set': {'preferences': data}}
    )
    
    log_activity('update_preferences', {
        'new_preferences': data
    })
    
    return jsonify({'message': 'Preferences updated successfully'})