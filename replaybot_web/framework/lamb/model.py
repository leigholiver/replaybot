import os, json, uuid, boto3, time

class model(object):
    # fields used by the model, not included in data obj 
    model_fields = [ 'table', 'fillable', 'data', 'indexes', 'sort_key', 'expires', 'db' ]
    db = None

    def __init__(self):
        self.setup_db()
        self.table = ""
        self.fillable = []
        self.indexes = []
        self.sort_key = ""
        self.expires = ""
        self.data = { 'id': str(uuid.uuid4()) }

    def setup_db(self):
        if self.db == None:
            # structured like this so we don't need tinydb in production
            if os.getenv('LAMB_ENV') == "local":
                from framework.lamb.db.localdb import localdb
                self.db = localdb()
            else:
                from framework.lamb.db.dynamodb import dynamodb
                self.db = dynamodb()

    # update fields as per self.fillable
    def update(self, data):
        tmp = {}
        for val in self.fillable:
            if val in data.keys():
                tmp[val] = data[val]
        self.data.update(tmp)

    # save to db
    def save(self):
        return self.db.save(self)
        
    # delete from db
    def delete(self):
        return self.db.delete(self)
    
    # get from db by id
    @classmethod
    def get(self, id):
        obj = self.get_model_obj()
        return self.db.get(obj, id)
    
    # find by index
    @classmethod
    def find(self, query):
        if len(query.keys()) != 1:
            print(query)
            return False
        obj = self.get_model_obj()
        for key in query.keys():
            value = query[key]
        return self.db.find(obj, key, value)

    @classmethod
    def list(self, direction = "asc", before = "", limit = 5):
        obj = self.get_model_obj()
        return self.db.list(obj, direction, before, limit)

    # set a ttl for the model
    def expire(self, ttl):
        self.expires = int(time.time()) + ttl

    def is_expired(self):
        return self.expires < time.time()

    # get the data object 
    def __dict__(self):
        return self.data

    # get the value from the data object, unless its a model key
    def __getattr__(self, name):
        if name not in self.model_fields:
            if name in self.data.keys():
                return self.data[name]
            return None
        else:
            return super().__getattr__(name)
    
    # set the data object, unless its a model key
    def __setattr__(self, name, value):
        if name not in self.model_fields:
            self.data[name] = value
        else:
            super().__setattr__(name, value)

        # partition key for sort
        if hasattr(self, "sort_key") and name == self.sort_key:
            self.__setattr__(self.sort_key + "_index", self.sort_key)

    def __str__(self):
        return json.dumps(self.data)
    
    # utility function to get model object from either tests folder or current models folder
    @classmethod
    def get_model_obj(self):
        self.setup_db(self)
        obj  = None
        name = self.__name__
        try:
            obj = getattr(__import__("framework.tests.support.models." + name, fromlist=[None]), name)
        except ModuleNotFoundError as e:
            obj = getattr(__import__("models." + name, fromlist=[None]), name)
        
        return obj