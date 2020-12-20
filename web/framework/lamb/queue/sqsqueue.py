import os, boto3, json
from framework.lamb.queue.queueinterface import queueinterface

class sqsqueue(queueinterface):

    def __init__(self, queue=None):
        super(sqsqueue, self).__init__(queue)
        self.queue = boto3.client('sqs')

    def enqueue(self, job):
        try:
            response = self.queue.send_message(
                QueueUrl=self.get_queue_url(),
                MessageBody=job
            )
            if response['MessageId']:
                tmp = json.loads(job)
                return tmp['id']
        except Exception as e:
            print(e)
        return False

    def get_jobs(self, limit = 10):
        jobs = []
        
        response = self.queue.receive_message(
            QueueUrl=self.get_queue_url(),
            MaxNumberOfMessages=limit
        )
        if 'Messages' in response.keys():
            for message in response['Messages']:
                rsp = self.queue.delete_message(
                    QueueUrl=self.get_queue_url(),
                    ReceiptHandle=message['ReceiptHandle']
                )
                jobs.append({'body': message['Body']})
        return {
            'Records': jobs
        }
    
    def get_queue_url(self):
        print(self.queue_name)
        response = self.queue.get_queue_url(QueueName=self.queue_name)
        return response['QueueUrl']