import os, json
from framework.lamb.command import command
from framework.util.hash_util import hash_util

class hashpath(command):
    def run(self, data):
        hasher = hash_util()
        if len(data) == 1:
            print(json.dumps({
                'result': hasher.hash_path(data[0]) if os.path.exists(data[0]) else "",
            }))
            return True

        print("please specify a file")
        return False