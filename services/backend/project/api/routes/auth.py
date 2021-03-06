from flask import Blueprint, jsonify, request
from sqlalchemy import exc, or_

from project import db, bcrypt
from project.api.models.blacklist_token import BlacklistToken
from project.api.models.user import User
from project.api.utils import authenticate
from project.api.utils import post_request


auth_blueprint = Blueprint('auth', __name__)


@auth_blueprint.route('/auth/register', methods=['POST'])
def register_user():
    post_data, response_object = post_request()

    from flask import current_app
    current_app.logger.info('/auth/register "post_data" %s', str(post_data))
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

    from flask import current_app
    current_app.logger.info('/auth/login "post_data" %s', str(post_data))
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
                    'user_id': user.id,
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
    post_data, response_object = post_request()

    from flask import current_app
    auth_token = request.headers.get('Authorization')
    current_app.logger.info('/auth/logout for auth_token: %s', str(auth_token))
    if auth_token:
        decoded_auth_token = User.decode_auth_token(auth_token=auth_token)
        if not isinstance(decoded_auth_token, str):
            blacklist_token = BlacklistToken(token=auth_token)
            try:
                db.session.add(blacklist_token)
                db.session.commit()
                response_object = {
                    'auth_token': auth_token,
                    'status': 'success',
                    'message': 'Successfully logged out.'
                }
                return jsonify(response_object), 200
            except Exception as e:
                response_object['message'] = e
                return jsonify(response_object), 500
        else:
            response_object['message'] = decoded_auth_token
            return jsonify(response_object), 401
    else:
        response_object['message'] = 'Provide valid auth token.'
        return jsonify(response_object), 403


@auth_blueprint.route('/auth/status', methods=['GET'])
@authenticate
def get_user_status(response):
    user = User.query.filter_by(id=response).first()

    from flask import current_app
    current_app.logger.info('/auth/status "user" %s', str(user))
    response_object = {
        'status': 'success',
        'message': 'Success.',
        'data': user.to_json(),
    }
    return jsonify(response_object), 200
