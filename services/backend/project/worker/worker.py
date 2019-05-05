from celery import Celery

from project.algorithms.crawl import Crawler
from project import crawlerdb

celery = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

mycol = crawlerdb["results"]


@celery.task(bind=True)
def execute_task(self, argument):
    self.update_state(state='STARTED', meta={'argument': argument})
    result = Crawler(item=argument).run()
    save_element = {"result": result}
    mycol.insert_one(save_element)
    return {'status': 'Task completed!', 'result': result}
