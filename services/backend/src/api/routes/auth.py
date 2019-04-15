from flask import Blueprint, jsonify
from sqlalchemy import exc, or_

from src import db, bcrypt
from src.api.models.user import User
from src.api.utils import authenticate
from src.api.utils import post_request


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    post_data, response_object = post_request()
    if not post_data:
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter(
            or_(User.username == username, User.email == email)
        ).first()
        if not user:
            new_user = User(
                username=username,
                email=email,
                password=password,
            )
            db.session.add(new_user)
            db.session.commit()

            auth_token = new_user.encode_auth_token(new_user.id)
            response_object['status'] = 'success'
            response_object['message'] = 'Successfully registered.'
            response_object['auth_token'] = auth_token.decode()
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'User already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_object), 400


@auth_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    post_data, response_object = post_request()
    if not post_data:
        return jsonify(response_object), 400

    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            auth_token = user.encode_auth_token(user.id)
            if auth_token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'auth_token': auth_token.decode(),
                }
                return jsonify(response_object), 200
        else:
            response_object['message'] = 'User does not exist.'
            return jsonify(response_object), 404
    except Exception:
        response_object['message'] = 'Try again.'
        return jsonify(response_object), 500


@auth_blueprint.route('/auth/logout', methods=['GET'])
@authenticate
def logout_user(response):
    response_object = {
        'status': 'success',
        'message': 'Successfully logged out.'
    }
    return jsonify(response_object), 200


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(response):
    user = User.query.filter_by(id=response).first()
    response_object = {
        'status': 'success',
        'message': 'Success.',
        'data': user.to_json(),
    }
    return jsonify(response_object), 200
