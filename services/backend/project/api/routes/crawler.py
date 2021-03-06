from flask import Blueprint, jsonify, url_for

from project import crawlerdb
from project.worker.worker import execute_task


crawler_blueprint = Blueprint('crawler', __name__)
tasks = crawlerdb.tasks
mycol = crawlerdb["results"]


@crawler_blueprint.route('/crawler/<phrase>', methods=['GET', 'POST'])
def longtask(phrase):

    from flask import current_app
    current_app.logger.info('/crawler/%s "Starting task..." %s', str(phrase))
    task = execute_task.apply_async((phrase,))

    current_app.logger.info('/crawler/%s "task.id" %s', str(task.id))
    return jsonify({
        'task_id': task.id,
        'Location': url_for('crawler.task_info', task_id=task.id)
    }), 202


@crawler_blueprint.route('/crawler_results', methods=['GET'])
def get_all_results():
    results = []
    for x in mycol.find():
        response_object = {
            'results': x,
        }
        results.append(response_object)
    return jsonify(results)


@crawler_blueprint.route('/crawler_info/<task_id>')
def task_info(task_id):
    task = execute_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'task_id': task_id,
            'state': task.state,
            'status': 'Pending...',
            'argument': task.info.get('argument'),

        }
    elif task.state != 'FAILURE':
        response = {
            'task_id': task_id,
            'state': task.state,
            'status': task.info.get('status', ''),
            'argument': task.info.get('argument'),
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'task_id': task_id,
            'state': task.state,
            'status': str(task.info),
            'argument': task.info.get('argument'),
        }
    return jsonify(response), 200
