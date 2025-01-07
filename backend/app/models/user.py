from datetime import datetime
from app.extensions import mongo, bcrypt

class User:
    @staticmethod
    def create(email, password):
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = {
            'email': email,
            'password': hashed_password,
            'preferences': {
                'theme': 'light',
                'notifications': 'enabled',
                'language': 'English'
            },
            'created_at': datetime.utcnow()
        }
        return mongo.db.users.insert_one(user)

    @staticmethod
    def get_by_email(email):
        return mongo.db.users.find_one({'email': email})