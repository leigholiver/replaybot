import datetime
from boto3.dynamodb.conditions import Key
from framework.lamb.model import model

class server(model):
    def __init__(self, id = None):
        super(server, self).__init__()
        
        # the name of the dynamodb table 
        self.table = "server"

        # discords server id
        self.id = id
        
        # the channel to put replies in
        # if "reply", will just reply to the message
        self.replyTo = "reply"

        # bot is currently in the server
        self.joined = False

        # channels to listen in, if empty, all channels
        self.listen = []

        # channels to ignore
        self.exclude = []

        # array of join/leave events
        self.events = []

        # cache of channels in the server
        self.channels = []

        self.fillable = [
            "replyTo",
            "listen",
            "exclude",
            "channels",
            "name",
            "icon"
        ]


    def join(self):
        self.joined = True
        self.events.append({
            "event": 'join',
            "timestamp": datetime.datetime.now().isoformat()    
        })

    def leave(self):
        self.joined = False
        self.events.append({
            "event": 'leave',
            "timestamp": datetime.datetime.now().isoformat()    
        })