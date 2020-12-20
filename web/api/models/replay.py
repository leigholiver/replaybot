import datetime
from framework.lamb.model import model

class replay(model):
    def __init__(self, guild = None, replay_data = None):
        super(replay, self).__init__()
        self.table    = "replay"
        self.fillable = [ "replay_data" ]
        self.indexes  = [ "guild" ]
        self.sort_key = "created"
        self.created  = datetime.datetime.now().isoformat()

        self.guild       = guild
        self.replay_data = replay_data
        self.indexed     = False