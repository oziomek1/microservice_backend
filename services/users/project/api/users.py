from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db


users_namespace = Blueprint('users', __name__)


@users_namespace.route('/users/ping', methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })


@users_namespace.route('/users', methods=['POST'])
def add_user():
    post_data = request.get_json()
    if not post_data:
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.',
        }
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!',
            }
            return jsonify(response_object), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Email already exists.',
            }
            return jsonify(response_object), 400
    except exc.IntegrityError:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload',
        }
        return jsonify(response_object), 400


@users_namespace.route('/users/<user_id>', methods=['GET'])
def get_single_user(user_id):
    response_object = {
        'status': 'fail',
        'message': 'User does not exist',
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()
        if not user:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': {
                    'id': user_id,
                    'username': user.username,
                    'email': user.email,
                    'active': user.active,
                },
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_namespace.route('/users', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()],
        },
    }
    return jsonify(response_object)


@users_namespace.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        db.session.add(User(username=username, email=email))
        db.session.commit()
    return jsonify({})
