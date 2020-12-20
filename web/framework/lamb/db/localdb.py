import os
from tinydb import TinyDB, Query
from framework.lamb.db.dbinterface import dbinterface
from framework.util.tinydb_util import lock, unlock
    
class localdb(dbinterface):
    # save the object
    def save(self, obj):
        lock(self.get_table_filename(obj))
        self.get_table(obj).upsert(obj.data, Query().id == obj.id)
        unlock(self.get_table_filename(obj))

    def batch_save(self, obj, items):
        for item in items:
            lock(self.get_table_filename(item))
            self.get_table(item).upsert(item.data, Query().id == item.id)
            unlock(self.get_table_filename(item))

    # delete the object from the db
    def delete(self, obj):
        lock(self.get_table_filename(obj))
        self.get_table(obj).remove(Query().id == obj.id)
        unlock(self.get_table_filename(obj))

    # get object by id
    def get(self, obj, id):
        tmp = obj()
        lock(self.get_table_filename(tmp))
        result = self.get_table(tmp).search(Query().id == id)
        unlock(self.get_table_filename(tmp))
        if len(result) == 1:
            tmp.data = dict(result[0])
            return tmp
        return False
    
    def batch_get(self, obj, ids):
        tmp = obj()
        lock(self.get_table_filename(tmp))
        result = self.get_table(tmp).search(Query().id.one_of(ids))
        unlock(self.get_table_filename(tmp))
        output = []
        for item in result:
            entity = obj()
            entity.data = dict(item)
            output.append(entity)
        return output

    # get a list of objects matching an index
    # {'index': 'search term'}
    def find(self, obj, key, value):
        tmp = obj()
        lock(self.get_table_filename(tmp))
        response = self.get_table(tmp).search(getattr(Query(), key) == value)
        unlock(self.get_table_filename(tmp))
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
        lock(self.get_table_filename(tmp))
        data = self.get_table(tmp).all()
        unlock(self.get_table_filename(tmp))
        
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

    def all(self, obj, key = None):
        tmp = obj()
        lock(self.get_table_filename(tmp))
        data = self.get_table(tmp).all()
        unlock(self.get_table_filename(tmp))
        output = []
        for item in data:
            entity = obj()
            entity.data = item
            output.append(entity)
        return {'key': None, 'items': output}

    def get_table(self, obj):
        os.system("mkdir -p .localdb")
        return TinyDB(self.get_table_filename(obj))

    def get_table_filename(self, obj):
        return "./.localdb/" + self.table_name(obj.table) + ".json"