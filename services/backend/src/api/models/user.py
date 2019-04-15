import datetime
import jwt

from flask import current_app
from sqlalchemy.sql import func

from src import db, bcrypt


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    created_date = db.Column(db.DateTime, default=func.now(), nullable=False)
    last_login_date = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUND')
        ).decode()

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(  # token expiration time
                    days=current_app.config.get('TOKEN_EXPIRATION_DAYS'),
                    seconds=current_app.config.get('TOKEN_EXPIRATION_SECONDS'),
                ),
                'iat': datetime.datetime.utcnow(),  # token generation time
                'sub': user_id,  # token subject
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256',
            )
        except Exception as ex:
            return ex

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Token expired. Log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Log in again.'

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'active': self.active,
            'created_date': self.created_date,
            'last_login_date': self.last_login_date,
        }
