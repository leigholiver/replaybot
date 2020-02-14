import os, requests
from support.lamb.Controller import Controller
from models.server import server
from models.creds import creds

API_ENDPOINT = 'https://discordapp.com/api'
GUILD_TEXT = 0 # indicator in discord api for text channel

class discord(Controller):

    def exchange_code(self, event):
        code = self.query(event, 'code')
        if not code:
            return self.respond(400, "Missing Discord Code")
        data = {
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': os.getenv('REDIRECT_URI'),
            'scope': 'identify guilds'
        }

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        r = self.request("POST", "/oauth2/token", headers, data)
        if r:
            response = r.json()
            auth = self.get_creds(response['access_token'], True)
            return self.respond(200, response)
        return self.respond(500, "Internal Server Error")

    def user_is_admin(self, guild, token):
        auth = self.get_creds(token)
        return guild in auth.guilds

    def get_creds(self, token, ignore_cache=False):
        auth = creds.get(token)
        if not auth:
            auth = creds(token)
        
        if auth.is_expired():
            headers = {
                'Authorization': "Bearer " + token,
                "content-type": "application/json"
            }
            r = self.request("GET", "/users/@me/guilds", headers)
            if r:
                servers = r.json()
                guilds = []
                for server in servers:
                    if (server['owner'] == True or (server['permissions'] & 0x00000008) == 0x00000008 or (server['permissions'] & 0x00000020) == 0x00000020):
                        guilds.append(server['id'])
        
                auth.guilds = guilds
                auth.set_expire()
                auth.save()
        return auth

    def get_guild_channels(self, event, guild):

        if not isinstance(event['headers'], dict) or "Authorization" not in event['headers'].keys():
            return self.respond(403, "Forbidden")

        if not self.user_is_admin(guild, event['headers']["Authorization"]):
            return self.respond(403, "Forbidden")

        headers = {
            'Authorization': "Bot " + os.getenv('BOT_TOKEN')
        }

        r = self.request("GET", "/guilds/%s/channels" % guild, headers)
        if r:
            data = r.json()
            out = []
            for channel in data:
                if channel['type'] == GUILD_TEXT:
                    out.append(channel)

            # cache the channels for next time 
            s = server.get(guild)
            if not s:
                s = server(id)
            s.channels = out

            return self.respond(200, out)
        return self.respond(500, "Internal Server Error")      

    def request(self, method, url, headers = None, data = None, auth=None):
        try:
            r = requests.request(method, API_ENDPOINT + url, data=data, headers=headers, auth=auth)
            r.raise_for_status()
            return r
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        return False