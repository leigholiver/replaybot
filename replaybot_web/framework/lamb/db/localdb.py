import os
from tinydb import TinyDB, Query
from framework.lamb.db.dbinterface import dbinterface
    
class localdb(dbinterface):
    # save the object
    def save(self, obj):
        self.get_table(obj).upsert(obj.data, Query().id == obj.id)

    # delete the object from the db
    def delete(self, obj):
        self.get_table(obj).remove(Query().id == obj.id)

    # get object by id
    def get(self, obj, id):
        tmp = obj()
        result = self.get_table(tmp).search(Query().id == id)
        if len(result) == 1:
            tmp.data = dict(result[0])
            return tmp
        return False

    # get a list of objects matching an index
    # {'index': 'search term'}
    def find(self, obj, key, value):
        tmp = obj()
        response = self.get_table(tmp).search(getattr(Query(), key) == value)
        output = []
        for item in response:
            entity = obj()
            entity.data = dict(item)
            output.append(entity)
        return output

    # list of objects
    # bad function, but this is just for development so not too fussed
    def list(self, obj, direction = "asc", before = "", limit = 5):
        tmp = obj()
        data = self.get_table(tmp).all()
        
        if before != "":
            data = list(filter(lambda d: d[tmp.sort_key] < before, data))

        data = sorted(data, key=lambda d: d[tmp.sort_key], reverse=(direction != "asc"))
        data = data[0:limit]

        output = []
        for item in data:
            entity = obj()
            entity.data = item
            output.append(entity)
        return output

    def get_table(self, obj):
        os.system("mkdir -p .localdb")
        return TinyDB("./.localdb/" + self.table_name(obj.table) + ".json")