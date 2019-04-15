from flask import Blueprint, jsonify

from src.api.models.admin import Admin


admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route('/admin', methods=['GET'])
def get_all_admins():
    response_object = {
        'status': 'success',
        'data': {
            'admin': [admin.to_json() for admin in Admin.query.all()],
        },
    }
    return jsonify(response_object)
