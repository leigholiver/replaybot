import os
from time import sleep
from framework.lamb.command import command
from framework.lamb.handlers.lambda_handler import lambda_handler
from framework.lamb.queue.queue_util import queue_util

class work(command):
    def run(self, data):
        print("working the local queue...")
        qu    = queue_util(os.getenv('testing'))
        go_on = True
        while go_on:
            try:
                sleep(0.05) # artificial delay just to make the thing responsive to stopping on ctrl c
                jobs = qu.get_jobs()
                if jobs != {'Records': []}:
                    print(jobs)
                    result = lambda_handler(jobs, {})
                    print(result)
            except KeyboardInterrupt:
                go_on = False
        return True