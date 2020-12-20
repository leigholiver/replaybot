import time
from framework.lamb.command import command
from models.replay import replay
from support.indexer import indexer

class index(command):
    def run(self, data):
        idx = indexer()

        # grab some replays
        if '--all' in data:
            replays = replay.all()['items']
        else:
            replays = replay.find({'indexed': False})
        
        # index them
        print("indexing " + str(len(replays)) + " replays...")
        for rep in replays:
            result = idx.index(rep)
            if result:
                rep.indexed = True
                rep.save()
            else:
                print("failed to index replay " + rep.id)

        # simples
        return True