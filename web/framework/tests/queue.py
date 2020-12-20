import os, json
from framework.lamb.test import test
from framework.lamb.queue.queue_util import queue_util
from framework.lamb.handlers.lambda_handler import lambda_handler

class queue(test):
    name = "queue"
    def run(self):
        qu    = queue_util('test')
        os.environ['testing'] = 'test'
        self.info("please stop the dev server before running this test")
        
        self.header("enqueue test")
        result = qu.enqueue({
            'class': 'framework.tests.support.commands.test_command',
            'function': 'run',
            'kwargs': {
                'data': ['arg1', 'arg2']
            }
        })
        self.record(result, "Success", "Success" if result else "Failure")
        
        self.header("execute test")
        result = lambda_handler(qu.get_jobs(), {})
        self.record(result, "Success", "Success" if result else "Failure")


        self.header("failure on bad job test")
        test_job_id = qu.enqueue({
            'class': 'some.nonexistent.namespace.class_name',
            'function': 'this_function_doesnt_exist',
            'kwargs': {
                'parameters': ['what', 'parameters?']
            }
        })
        jobs = qu.get_jobs()
        
        result = lambda_handler(jobs, {})
        self.record(not result, "Failure", "Failure" if result else "Success")
        
        self.header("max attempts test")
        success = True
        # work through the failures
        for i in range(1, qu.max_attempts):
            if not self.is_still_there(qu, test_job_id):
                self.info("test id is gone before max_attempts hit")
                success = False

        # failed job should be gone
        if self.is_still_there(qu, test_job_id):
            self.info("test id is still there after max_attempts hit")
            success = False
        self.record(success, "Success", "Success" if success else "Failure")

        return self.successful


    def is_still_there(self, qu, test_job_id):
        still_there = False
        jobs = qu.get_jobs()
        for job in jobs['Records']:
            tmp = json.loads(job['body'])
            if tmp['id'] == test_job_id:
                still_there = True
        lambda_handler(jobs, {})
        return still_there