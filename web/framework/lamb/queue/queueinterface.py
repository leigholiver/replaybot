import os

class queueinterface():
    def __init__(self, queue=None):
        self.queue_name = os.getenv('PROJECT_NAME') + "_" + os.getenv('LAMB_ENV') + "_" + ("job" if queue == None else queue) + "_queue"

    # queue a job
    # job should be a dict like:
    # {
    #     'class': 'commands.example',
    #     'function': 'run',
    #     'kwargs': {
    #        'data': ['arg1', 'arg2']
    #      }
    # }
    def enqueue(self, job):
        return False