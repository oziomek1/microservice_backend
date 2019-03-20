from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project.api.admins import Admin
from project.api.utils import authenticate
from project.api.utils import is_admin
from project.api.utils import post_request
from project import db


users_blueprint = Blueprint('users', __name__)


@users_blueprint.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db.session.add(User(username=username, email=email, password=password))
        db.session.commit()
    return jsonify({})


@users_blueprint.route('/users/ping', methods=['GET'])
def ping():
    return jsonify({
        'status': 'success',
        'message': 'ping!'
    })


@users_blueprint.route('/users', methods=['POST'])
@authenticate
def add_user(response):
    post_data, response_object = post_request()
    if not is_admin(response):
        response_object['message'] = 'No permission.'
        return jsonify(response_object), 401
    if not post_data:
        return jsonify(response_object), 400

    username = post_data.get('username')
    email = post_data.get('email')
    password = post_data.get('password')
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email, password=password))
            db.session.commit()
            response_object = {
                'status': 'success',
                'message': f'{email} was added!',
            }
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Email already exists.'
            return jsonify(response_object), 400
    except (exc.IntegrityError, ValueError):
        db.session.rollback()
        return jsonify(response_object), 400


@users_blueprint.route('/users/<user_id>', methods=['GET'])
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
                'data': user.to_json(),
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404

@users_blueprint.route('/admins/<admin_id>', methods=['GET'])
def get_single_admin(admin_id):
    response_object = {
        'status': 'fail',
        'message': 'Admin does not exist',
    }
    try:
        admin = Admin.query.filter_by(id=int(admin_id)).first()
        if not admin:
            return jsonify(response_object), 404
        else:
            response_object = {
                'status': 'success',
                'data': admin.to_json(),
            }
            return jsonify(response_object), 200
    except ValueError:
        return jsonify(response_object), 404


@users_blueprint.route('/users', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'users': [user.to_json() for user in User.query.all()],
        },
    }
    return jsonify(response_object)

@users_blueprint.route('/admins', methods=['GET'])
def get_all_admins():
    response_object = {
        'status': 'success',
        'data': {
            'admins': [admin.to_json() for admin in Admin.query.all()],
        },
    }
    return jsonify(response_object)