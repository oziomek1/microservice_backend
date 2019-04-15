from enum import Enum


class TaskStatus(Enum):
    CREATED = 'Created'
    DONE = 'Done'
    FAILED = 'Failed'
    RUNNING = 'Running'
