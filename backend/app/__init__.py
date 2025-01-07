from flask import Flask
from flask_cors import CORS
from app.extensions import mongo, bcrypt
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app, supports_credentials=True)
    mongo.init_app(app)
    bcrypt.init_app(app)
    
    # Register blueprints
    from app.routes import auth, preferences, session
    app.register_blueprint(auth.bp)
    app.register_blueprint(preferences.bp)
    app.register_blueprint(session.bp)
    
    return app