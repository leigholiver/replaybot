import os, json
from framework.lamb.handlers.handlerinterface import handlerinterface
from framework.lamb.queue.queue_util import queue_util

class queue(handlerinterface):
    def is_valid(self, event):
        if isinstance(event, dict) and "Records" in event.keys():
            return True
        return False

    def handle(self, event, context):
        failed_jobs = []
        for record in event['Records']:
            try:
                record = json.loads(record['body'])
                obj  = self.get_job_obj(record['body']['class'])
                obj = obj()
                func = getattr(obj, record['body']['function'])
                result = func(**record['body']['kwargs'])
                if not result:
                    raise Exception("no result")
            except ValueError as e:
                print("abandoning invalid job: " + str(record))
            except Exception as e:
                err = str(type(e)) + " " + str(e)
                print("error running job " + record['id'] + ": " + err)
                record['error'] = err
                failed_jobs.append(record)
        
        if failed_jobs != []:            
            qu = queue_util(os.getenv('testing'))
            abandoned_jobs = []
            for job in failed_jobs:
                result = qu.requeue(job)
                if not result:
                    abandoned_jobs.append(job)

            if abandoned_jobs != []:
                print("abandoned jobs: " + str(abandoned_jobs))

            return False
        return True

    def get_job_obj(self, name):
        obj = None
        try:
            obj = getattr(__import__(name, fromlist=[None]), name.split(".")[-1])
        except ModuleNotFoundError as e:
            raise Exception("couldnt find job class")
        return obj