import datetime
from framework.lamb.model import model

class user(model):
    def __init__(self, id=None):
        super(user, self).__init__()
        self.table = "user"
        self.sort_key      = 'last_updated'
        self.set_updated()

        self.id            = id # discord user id
               
        # meta
        self.username      = "" # discord username
        self.discriminator = "" # discord user discriminator
        self.avatar        = "" # discord avatar hash

        # auth
        self.access_token  = "" # discord oauth access token
        self.token_expires = "" # expiry timestamp for the token
        self.refresh_token = "" # discord oauth refresh token

        # servers
        self.guilds        = [] # guild ids the user is in
        self.admin_guilds  = [] # guild ids the user has admin permissions in



    def set_updated(self):
        self.last_updated = datetime.datetime.now().isoformat()