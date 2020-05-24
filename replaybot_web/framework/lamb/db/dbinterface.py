import os

class dbinterface():
    # get environment formatted table name from model name
    def table_name(self, model_name):
        return os.getenv('PROJECT_NAME') + "_" + os.getenv('LAMB_ENV') + "_" + model_name

    # save the object
    def save(self, obj):
        pass

    # delete the object from the db
    def delete(self, obj):
        pass

    # get object by id
    def get(self, obj, id):
        pass

    # get a list of objects matching an index
    def find(self, obj, key, value):
        pass 

    # list of objects
    def list(self, obj, direction = "asc", before = "", limit = 5):
        pass
