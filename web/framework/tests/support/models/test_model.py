import time, datetime
from framework.lamb.model import model

class test_model(model):
    def __init__(self):
        super(test_model, self).__init__()
        
        self.table = "test_model"
        self.indexes = ["test_index"]
        self.sort_key = "created"
        self.created = datetime.datetime.now().isoformat()