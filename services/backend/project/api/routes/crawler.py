from flask import Blueprint, jsonify, request
from pymongo import errors

from project.api.utils import post_request
from project.api.models.task import Task
from project import crawlerdb


crawler_blueprint = Blueprint('crawler', __name__)
tasks = crawlerdb.tasks


@crawler_blueprint.route('/crawler', methods=['GET', 'POST'])
def start_crawl():
    if request.method == "GET":
        response_object = {
            'status': 'success',
            'data': {
                'task': tasks.find_one({}),
            },
        }
        return jsonify(response_object), 200
    post_data, response_object = post_request()
    if not post_data:
        return jsonify(response_object), 400

    search_item = post_data.get('item')
    task = Task.create_task(id=1, item=search_item)
    try:
        tasks.insert_one(jsonify(task))
    except errors.DuplicateKeyError:
        return jsonify('DuplicateKeyError'), 404

    response_object['status'] = 'success'
    response_object['message'] = 'Successfully passed item {}, task_id {}'.format(search_item, task.id)
    return jsonify(response_object), 201
