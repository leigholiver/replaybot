import os, requests, time
from models.user import user as user_model
from models.server import server as server_model

API_ENDPOINT  = 'https://discordapp.com/api'
GUILD_TEXT    = 0            # indicator in discord api for text channel
ADMINISTRATOR = 0x00000008   # permissions
MANAGE_GUILD  = 0x00000020   # permissions
VIEW_CHANNEL  = 0x00000400   # permissions

# todo: should the discord util be saving users/guids?
class discord():
    def get_user_visible_channels(self, user):
        output = [os.getenv("PUBLIC_CHANNEL_ID")]
        for guild in user.guilds:
            g = server_model.get(guild)
            if g:
                for channel in g.channels.keys():
                    if self.user_can_see_channel(g, user.id, channel):
                        output.append(channel)
        return output

    def user_can_see_channel(self, server, userid, channelid):
        # @everyone permissions
        permissions = server.base_permissions
        if userid in server.member_roles.keys():
            for role in server.member_roles[userid]:
                permissions |= server.roles[role]
        allow = 0
        deny  = 0
        for overwrite in server.channels[channelid]['permissions']:
            # everyone role overwrite
            if overwrite['type'] == "role" and overwrite['id'] == server.everyone_role_id:
                allow |= overwrite['allow']
                deny  |= overwrite['deny']
            # member role overwrites
            if userid in server.member_roles.keys() and overwrite['type'] == "role" and overwrite['id'] in server.member_roles[userid]:
                allow |= overwrite['allow']
                deny  |= overwrite['deny']
            # member overwrites
            if overwrite['type'] == "member" and overwrite['id'] == userid:
                allow |= overwrite['allow']
                deny  |= overwrite['deny']
        permissions &= ~deny
        permissions |= allow
        return (permissions & VIEW_CHANNEL) == VIEW_CHANNEL

    def update_guild_meta_by_id(self, serverid):
        server = server_model.get(serverid)
        if not server:
            server = server_model(serverid)
        self.update_guild_meta(server)
        return True

    def update_guild_meta(self, server):
        if server.joined:
            headers = {'Authorization': "Bot " + os.getenv('BOT_TOKEN'), "content-type": "application/json"}
            r = self.request("GET", "/guilds/%s" % server.id, headers)
            if r:
                guild = r.json()

                # update the meta
                server.name = guild['name']
                server.icon = guild['icon']

                # update the roles/permissions
                roles = {}
                for role in guild['roles']:
                    if role['name'] == '@everyone':
                        server.base_permissions = role['permissions']
                        server.everyone_role_id = role['id']
                    else:
                        roles[role['id']] = role['permissions']
                server.roles = roles

                # update channels/members for permissions
                if not self.update_guild_channels(server):
                    print("failed to update channels for %d (%s)" % (server.id, server.name))
                if not self.update_guild_members(server):
                    print("failed to update members for %d (%s)" % (server.id, server.name))
                server.set_updated()
                server.save() # todo: why do we save here but not in others?
                return True
        server.set_updated()
        server.save()
        print("failed to guild meta for %s (%s)" % (server.id, server.name))
        return False

    def update_guild_channels(self, server):
        headers = {'Authorization': "Bot " + os.getenv('BOT_TOKEN'), "content-type": "application/json"}
        r = self.request("GET", "/guilds/%s/channels" % server.id, headers)
        if r:
            channels = {}
            chans    = r.json()
            for channel in chans:
                if channel['type'] == GUILD_TEXT:
                    channels[channel['id']] = {
                        'id':          channel['id'],
                        'name':        channel['name'],
                        'permissions': channel['permission_overwrites']
                    }
            server.channels = channels
            server.set_updated()
            return True
        return False

    def update_guild_members(self, server):
        headers = {'Authorization': "Bot " + os.getenv('BOT_TOKEN'), "content-type": "application/json"}
        r = self.request("GET", "/guilds/%s/members?limit=1000" % server.id, headers)
        if r:
            guild_members = r.json()
            member_roles  = {}
            for member in guild_members:
                member_roles[member['user']['id']] = member['roles']
            server.member_roles = member_roles
            server.set_updated()
            return True
        return False

    def update_user_meta(self, user):
        headers = {'Authorization': "Bearer " + user.access_token, "content-type": "application/json"}
        r = self.request("GET", "/users/@me", headers)
        if r:
            u                  = r.json()
            user.avatar        = u['avatar']
            user.discriminator = u['discriminator']
            user.username      = u['username']
            user.set_updated()
            user.save() # todo: why do we save here but not in the others?
            return True
        return False

    def update_user_guilds(self, user):
        headers = {'Authorization': "Bearer " + user.access_token, "content-type": "application/json"}
        r = self.request("GET", "/users/@me/guilds", headers)
        if r:
            servers      = r.json()
            admin_guilds = []
            guilds       = []
            for server in servers:
                guilds.append(server['id'])
                if (server['owner'] == True or (server['permissions'] & ADMINISTRATOR) == ADMINISTRATOR or (server['permissions'] & MANAGE_GUILD) == MANAGE_GUILD):
                    admin_guilds.append(server['id'])
            user.admin_guilds = admin_guilds
            user.guilds       = guilds
            user.set_updated()
            self.update_partial_guild_meta(servers, guilds)
        return user

    def update_partial_guild_meta(self, servers, serverids):
        seen_servers = server_model.batch_get(serverids)
        batch = []
        for server in servers:
            tmp = next((item for item in seen_servers if item.id == server['id']), None)
            if not tmp:
                tmp = server_model(server['id'])
            if tmp.name != server['name'] or tmp.icon != server['icon']:
                tmp.name = server['name']
                tmp.icon = server['icon']
                batch.append(tmp)
        server_model.batch_save(batch)

    def handle_code(self, code):
        access_token = self.get_access_token(code)
        if not access_token:
            return False
        return self.update_user_token(access_token)

    def refresh_user_token(self, user):
        refresh_token = self.get_refresh_token(user.refresh_token)
        if not refresh_token:
            return False
        return self.update_user_token(refresh_token)

    def update_user_token(self, token):
        # find the user
        headers = {'Authorization': "Bearer " + token['access_token'], "content-type": "application/json"}
        r = self.request("GET", "/users/@me", headers)
        if not r:
            return False

        u = r.json()
        user = user_model.get(u['id'])
        if not user:
            user = user_model(u['id'])
            user.avatar        = u['avatar']
            user.discriminator = u['discriminator']
            user.username      = u['username']

        # set the auth
        user.access_token  = token['access_token']
        user.refresh_token = token['refresh_token']
        user.token_expires = int(time.time()) + int(token['expires_in'])
        user = self.update_user_guilds(user)
        user.save()
        return user

    def get_access_token(self, code):
        return self.exchange_code({'grant_type': 'authorization_code', 'code': code })

    def get_refresh_token(self, refresh_token):
        return self.exchange_code({'grant_type': 'refresh_token', 'refresh_token': refresh_token})

    def exchange_code(self, params):
        data = {
            'client_id': os.getenv('CLIENT_ID'),
            'client_secret': os.getenv('CLIENT_SECRET'),
            'redirect_uri': os.getenv("REDIRECT_URI"),
            'scope': 'identify guilds'
        }
        data.update(params)
        r = self.request("POST", "/oauth2/token", {'Content-Type': 'application/x-www-form-urlencoded'}, data)
        if r:
            return r.json()
        return False

    def request(self, method, url, headers = None, data = None, auth=None):
        try:
            r = requests.request(method, API_ENDPOINT + url, data=data, headers=headers, auth=auth)
            r.raise_for_status()
            return r
        except Exception as err:
            print(err)
            print(r.json())
        return False
