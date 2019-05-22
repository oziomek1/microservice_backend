from functools import wraps
from flask import jsonify, request

from project import db
from project.api.models.user import User


def authenticate(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        response_object = {
            'status': 'fail',
            'message': 'Provide valid auth token.',
        }
        code = 401
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            code = 403
            return jsonify(response_object), code
        decoded_auth_token = User.decode_auth_token(auth_token)
        if isinstance(decoded_auth_token, str):
            response_object['message'] = decoded_auth_token
            return jsonify(response_object), code
        user = User.query.filter_by(id=decoded_auth_token).first()
        if not user or not user.active:
            return jsonify(response_object), code
        return func(decoded_auth_token, *args, **kwargs)
    return decorated_function


def post_request():
    post_data = request.get_json()
    response_object = {
        'status': 'fail',
        'message': 'Invalid payload.'
    }
    return post_data, response_object


def add_admin_user(username, email, password):
    user = User(
        username=username,
        email=email,
        password=password,
    )
    db.session.add(user)
    db.session.commit()

    user = User.query.filter_by(email=email).first()
    user.admin = True
    db.session.commit()
    return user
