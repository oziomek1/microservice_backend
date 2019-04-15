from project.api.enums.task_status import TaskStatus


class Task:
    def __init__(self, id, item, status=TaskStatus.CREATED):
        self.id = id
        self.item = item
        self.status = status

    @staticmethod
    def create_task(id, item):
        task = Task(id=id, item=item)
        return task
