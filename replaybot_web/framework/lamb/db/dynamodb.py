import os, boto3
from boto3.dynamodb.conditions import Key
from framework.lamb.db.dbinterface import dbinterface

class dynamodb(dbinterface):
    # for dynamodb local
    local_db_endpoint = 'http://localhost:8000' if os.getenv('LAMB_ENV') == 'localdb' else None
    
    # save the object
    def save(self, obj):
        self.get_table(obj).put_item(Item = obj.data)

    # delete the object from the db
    def delete(self, obj):
        self.get_table(obj).delete_item(Key={ 'id': obj.id })

    # get object by id
    def get(self, obj, id):
        tmp = obj()
        result = self.get_table(tmp).get_item(Key={ 'id': id })
        if 'Item' not in result.keys():
            return False
        tmp.data = result['Item']
        return tmp

    # get a list of objects matching an index
    # {'index': 'search term'}
    def find(self, obj, key, value):
        tmp = obj()
        response = self.get_table(tmp).query(
            IndexName=key + "_index",
            KeyConditionExpression=Key(key).eq(value)
        )

        output = []
        for item in response['Items']:
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    # list of objects
    def list(self, obj, direction = "asc", before = "", limit = 5):
        tmp = obj()
        sort_key = tmp.sort_key
        exp = Key(sort_key + '_index').eq(sort_key)
        if before != "":
            exp = exp & Key(sort_key).lt(before)
        
        response = self.get_table(tmp).query(
            IndexName = sort_key + "_sort",
            KeyConditionExpression = exp,
            Limit = limit,
            ScanIndexForward= direction == "asc"
        )

        output = []
        for item in response['Items']:
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    def get_table(self, obj):
        client = boto3.resource('dynamodb', endpoint_url=self.local_db_endpoint)
        table = client.Table(self.table_name(obj.table))
        return table