from support.lamb.Model import Model

class replay(Model):
    def __init__(self, guild = None, replay_data = None):
        super(replay, self).__init__()
        
        # the name of the dynamodb table 
        self.table = "replay"

        # list of str, fields which are allowed
        # to be updated from the api
        self.fillable = [ "replay_data" ]

        # list of fields to use as string 
        # indexes you will be able to use 
        # these as parameters for replay.find()
        self.indexes = [ "guild" ]

        self.guild = guild
        self.replay_data = replay_data