import datetime
from framework.lamb.model import model
from framework.lamb.queue.queue_util import queue_util

class server(model):
    def __init__(self, id = None):
        super(server, self).__init__()
        self.table            = "server"
        self.sort_key         = 'last_updated'
        self.set_updated()

        self.id               = id      # discords server id
        self.joined           = False   # bot is currently in the server
        self.replyTo          = "reply" # the channel to put replies in, if "reply", will just reply to the message
        self.listen           = []      # channels to listen in, if empty, all channels
        self.exclude          = []      # channels to ignore
        self.events           = []      # array of join/leave events
        self.channels         = {}      # cache of channels in the server
        self.base_permissions = 0       # permissions of the @everyone role
        self.everyone_role_id = ""      # id of the @everyone role
        self.roles            = {}      # role id/permissions for calculating channel visibility
        self.member_roles     = {}      # map of members:roles for calculating channel visibility
        
        self.fillable = [
            "replyTo",
            "listen",
            "exclude"
        ]

    def set_updated(self):
        self.last_updated = datetime.datetime.now().isoformat()

    def join(self):
        self.joined = True
        self.events.append({
            "event": 'join',
            "timestamp": datetime.datetime.now().isoformat()    
        })

        qu    = queue_util()
        result = qu.enqueue({
            'class': 'support.discord',
            'function': 'update_guild_meta_by_id',
            'kwargs': {'serverid': self.id}
        })

    def leave(self):
        self.joined = False
        self.events.append({
            "event": 'leave',
            "timestamp": datetime.datetime.now().isoformat()    
        })