import json, uuid, boto3
from boto3.dynamodb.conditions import Key

class Model(object):

    def __init__(self):
        self.table = ""
        self.fillable = []
        self.indexes = []
        self.sort_key = ""
        self.data = { 'id': str(uuid.uuid4()) }

    def getTable(self):
        client = boto3.resource('dynamodb')
        table = client.Table(self.table)
        return table

    # update fields as per self.fillable
    def update(self, data):
        tmp = {}
        for val in self.fillable:
            if val in data.keys():
                tmp[val] = data[val]
        self.data.update(tmp)

    # save to db
    def save(self):
        table = self.getTable()
        table.put_item(Item = self.data)

    def delete(self):
        table = self.getTable()
        table.delete_item(
            Key={
                'id': self.id
            }
        )

    # get from db by id
    @classmethod
    def get(self, id):
        obj = getattr(getattr(__import__("models." + self.__name__), self.__name__), self.__name__)
        obj = obj()
        table = obj.getTable()
        tmp = table.get_item(Key={
            'id': id
        })
        if 'Item' not in tmp.keys():
            return False

        obj.data = tmp['Item']
        return obj
    
    # find by index
    @classmethod
    def find(self, query):
        if len(query.keys()) != 1:
            print(query)
            return False

        obj = getattr(getattr(__import__("models." + self.__name__), self.__name__), self.__name__)
        entity = obj()
        table = entity.getTable()
        
        for key in query.keys():
            key = key
            value = query[key]
            
        response = table.query(
            IndexName=key + "_index",
            KeyConditionExpression=Key(key).eq(value)
        )

        output = []
        for item in response['Items']:
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    def __dict__(self):
        return self.data

    def __getattr__(self, name):
        if name not in [ 'table', 'fillable', 'data', 'indexes', 'sort_key']:
            if name in self.data.keys():
                return self.data[name]
            return None
        else:
            return super().__getattr__(name)
    
    def __setattr__(self, name, value):
        if name not in [ 'table', 'fillable', 'data', 'indexes', 'sort_key' ]:
            self.data[name] = value
        else:
            super().__setattr__(name, value)

    def __str__(self):
        return json.dumps(self.data)
    