from flask import Blueprint, jsonify
from sqlalchemy import exc

from project.api.models.user import User
from project.api.models.admin import Admin
from project.api.utils import authenticate
from project.api.utils import post_request
from project import db


user_blueprint = Blueprint('user', __name__)


@user_blueprint.route('/user', methods=['POST'])
@authenticate
def add_user(response):
    post_data, response_object = post_request()

    from flask import current_app
    current_app.logger.info('/user/[POST] "post_data" %s', str(post_data))
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


@user_blueprint.route('/user/<user_id>', methods=['GET'])
def get_single_user(user_id):
    response_object = {
        'status': 'fail',
        'message': 'User does not exist',
    }
    try:
        user = User.query.filter_by(id=int(user_id)).first()

        from flask import current_app
        current_app.logger.info('/user/%s "user" %s', str(user_id), str(user))
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


@user_blueprint.route('/admin/<admin_id>', methods=['GET'])
def get_single_admin(admin_id):
    response_object = {
        'status': 'fail',
        'message': 'Admin does not exist',
    }
    try:
        admin = Admin.query.filter_by(id=int(admin_id)).first()

        from flask import current_app
        current_app.logger.info('/admin/%s "admin" %s', str(admin_id), str(admin))
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


@user_blueprint.route('/user', methods=['GET'])
def get_all_users():
    response_object = {
        'status': 'success',
        'data': {
            'user': [user.to_json() for user in User.query.all()],
        },
    }
    return jsonify(response_object)
