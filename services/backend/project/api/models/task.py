from project.api.enums.task_status import TaskStatus


class Task:
    def __init__(self, id, argument, status=TaskStatus.CREATED):
        self.id = id
        self.argument = argument
        self.status = status

    @staticmethod
    def create_task(id, argument):
        task = Task(id=id, argument=argument)
        return task
