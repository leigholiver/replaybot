import os

class dbinterface():
    # get environment formatted table name from model name
    def table_name(self, model_name):
        return os.getenv('PROJECT_NAME') + "_" + os.getenv('LAMB_ENV') + "_" + model_name

    # save the object
    def save(self, obj):
        pass
    
    #
    def batch_save(self, obj, items):
        pass
    
    # delete the object from the db
    def delete(self, obj):
        pass

    # get object by id
    def get(self, obj, id):
        pass
    
    # get multiple objects by a list of ids
    def batch_get(self, obj, ids):
        pass
    
    # get a list of objects matching an index
    def find(self, obj, key, value):
        pass 

    # list of objects
    def list(self, obj, direction = "asc", before = "", limit = 5):
        pass
    
    # equivalent of a dynamodb scan
    # should return a dict as:
    # {
    #     key: None,  # the key to continue the scan from, if required
    #     items: []   # the returned items
    # }
    def all(self, obj, key = None):
        pass
