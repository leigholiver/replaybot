import os, boto3, decimal
from boto3.dynamodb.conditions import Key
from framework.lamb.db.dbinterface import dbinterface

class dynamodb(dbinterface):
    # for dynamodb local
    local_db_endpoint = 'http://localhost:8000' if os.getenv('LAMB_ENV') == 'localdb' else None

    # save the object
    def save(self, obj):
        self.get_table(obj).put_item(Item = obj.data)

    def batch_save(self, obj, items):
        tmp = obj()
        with self.get_table(tmp).batch_writer() as batch:
            for item in items:
                batch.put_item(Item=item.data)

    # delete the object from the db
    def delete(self, obj):
        self.get_table(obj).delete_item(Key={ 'id': obj.id })

    # get object by id
    def get(self, obj, id):
        tmp = obj()
        result = self.get_table(tmp).get_item(Key={ 'id': id })
        if 'Item' not in result.keys():
            return False
        tmp.data = self.process_items(result['Item'])
        return tmp

    def batch_get(self, obj, ids):
        keys = []
        for id in ids:
            keys.append({ 'id': id })
        tmp = obj()
        result = self.get_client().batch_get_item(RequestItems={ self.table_name(tmp.table): {'Keys': keys} })
        output = []
        for item in self.process_items(result['Responses'][self.table_name(tmp.table)]):
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    # get a list of objects matching an index
    # {'index': 'search term'}
    def find(self, obj, key, value):
        tmp = obj()
        response = self.get_table(tmp).query(
            IndexName=key + "_index",
            KeyConditionExpression=Key(key).eq(value)
        )

        output = []
        for item in self.process_items(response['Items']):
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
        for item in self.process_items(response['Items']):
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    def all(self, obj, key = None):
        output   = {}
        tmp      = obj()
        response = self.get_table(tmp).scan(ExclusiveStartKey=key)
        output['items'] = self.process_items(response['Items'])
        if 'LastEvaluatedKey' in response:
            output['key'] = response['LastEvaluatedKey']
        return output

    # https://github.com/boto/boto3/issues/369#issuecomment-157205696
    def process_items(self, obj):
        if isinstance(obj, list):
            return [self.process_items(i) for i in obj]
        elif isinstance(obj, dict):
            return {k: self.process_items(v) for k, v in obj.items()}
        elif isinstance(obj, decimal.Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return obj

    def get_table(self, obj):
        client = self.get_client()
        table = client.Table(self.table_name(obj.table))
        return table

    def get_client(self):
        return boto3.resource('dynamodb', endpoint_url=self.local_db_endpoint)
