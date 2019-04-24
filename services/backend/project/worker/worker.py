from celery import Celery

from project.algorithms.crawl import Crawler


celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')


@celery.task(bind=True)
def execute_task(self, argument):
    self.update_state(state='STARTED', meta={'argument': argument})
    result = Crawler(item=argument).run()
    return {'status': 'Task completed!', 'result': result}
