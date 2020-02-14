import time
from support.lamb.Model import Model

class creds(Model):
    def __init__(self, id=None):
        super(creds, self).__init__()
        
        # the name of the dynamodb table 
        self.table = "creds"

        self.id = id
        self.expires = 0

    def is_expired(self):
        return self.expires < time.time()

    def set_expire(self):
        self.expires = int(time.time()) + 300