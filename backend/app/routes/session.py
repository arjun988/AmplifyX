from flask import Blueprint, request, jsonify, session
from datetime import datetime
from app.utils.decorators import login_required
from app.utils.logger import log_activity
from app.extensions import mongo

bp = Blueprint('session', __name__, url_prefix='/api')

@bp.route('/session/page', methods=['POST'])
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
    
    log_activity('page_visit', {'page': page})
    
    return jsonify({'message': 'Page visit logged'})

@bp.route('/session', methods=['GET'])
@login_required
def get_session_info():
    if 'start_time' not in session:
        return jsonify({'error': 'No active session'}), 404
    
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    pages_visited = session.get('pages_visited', [])
    total_pages = len(pages_visited)
    total_pages_count = (total_pages + per_page - 1) // per_page
    
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

@bp.route('/activities', methods=['GET'])
@login_required
def get_activities():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    total_activities = mongo.db.activities.count_documents({
        'user_id': session['user_id']
    })
    
    activities = mongo.db.activities.find(
        {'user_id': session['user_id']},
        {'_id': 0}
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