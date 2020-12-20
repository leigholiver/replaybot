import os, json, sys
from tinydb import TinyDB, Query
from framework.lamb.queue.queueinterface import queueinterface
from framework.util.tinydb_util import lock, unlock

# simple queue for local dev purposes, not production safe at all
class tinydbqueue(queueinterface):
    def enqueue(self, job):
        lock(self.get_table_filename())
        try:
            self.get_jobs_table().insert(json.loads(job))
            unlock(self.get_table_filename())
            return True
        except Exception as e:
            print(e)

        unlock(self.get_table_filename())
        return False

    def get_jobs(self, limit = 25):
        jobs = []
        lock(self.get_table_filename())
        try:
            jobs = self.get_jobs_table().all()[0:limit]
            for job in jobs:
                self.get_jobs_table().remove(Query().id == job['id'])
        except Exception as e:
            print(str(e))
        unlock(self.get_table_filename())

        out = []
        for job in jobs:
            out.append({'body': json.dumps(job)})

        return {
            'Records': out
        }

    def get_table_filename(self):
        return "./.localdb/" + self.queue_name + ".json"

    def get_jobs_table(self):
        os.system("mkdir -p .localdb")
        return TinyDB(self.get_table_filename())