import os
from datetime import timedelta

class Config:
    MONGO_URI = 'mongodb://localhost:27017/squid'
    SECRET_KEY = os.urandom(24)
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # Set to True in production
    SESSION_COOKIE_SAMESITE = 'Lax'