from framework.lamb.model import model

CREDS_TTL = 300

class creds(model):
    def __init__(self, id=None):
        super(creds, self).__init__()
        self.table = "creds"
        self.id = id
        self.expire(0)

    def set_expire(self):
        self.expire(CREDS_TTL)