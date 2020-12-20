import os, uuid, json

class queue_util():
    # todo: max attempts var in queue util
    max_attempts = 5
    
    def __init__(self, queue=None):
        # structured like this so we don't need tinydb in production
        if os.getenv('LAMB_ENV') == "local":
            from framework.lamb.queue.tinydbqueue import tinydbqueue
            self.queue = tinydbqueue(queue)
        else:
            from framework.lamb.queue.sqsqueue import sqsqueue
            self.queue = sqsqueue(queue)

    # job_data should be a dict like:
    # {
    #     'class': 'example', # this should be a class in the jobs namespace? or just whatever?
    #     'function': 'run',
    #     'kwargs': { 'data': ['arg1', 'arg2'] }
    # }
    def enqueue(self, job_data):
        job = {
            'id':       str(uuid.uuid4()),
            'body':     job_data,
            'attempts': 0
        }
        if not self.queue.enqueue(json.dumps(job)):
            return False
        return job['id']

    def requeue(self, job):
        job['attempts'] += 1
        if job['attempts'] >= self.max_attempts:
            return False
        if not self.queue.enqueue(json.dumps(job)):
            return False
        return job['id']

    def get_jobs(self, limit = 10):
        return self.queue.get_jobs(limit)