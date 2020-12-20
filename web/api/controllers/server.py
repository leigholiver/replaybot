from framework.lamb.controller import controller
from models.server import server as m_server
from middleware.hasbottoken import hasbottoken

class server(controller):
    def user_servers(self, event):
        user = event['logged_in_user']
        servers = []
        for server in m_server.batch_get(user.guilds):
            channels = []
            for channel in server.channels.keys():
                channels.append({'id': server.channels[channel]['id'], 'name': server.channels[channel]['name']})
            # filter out some fields
            servers.append({
                'id':       server.id,
                'name':     server.name,
                'admin':    server.id in user.admin_guilds,
                'icon':     server.icon,
                'joined':   server.joined,
                'replyTo':  server.replyTo,
                'listen':   server.listen,
                'exclude':  server.exclude,
                'channels': channels,
                'events':   server.events
            })
        output = {
            'id':            user.id,
            'username':      user.username,
            'discriminator': user.discriminator,
            'avatar':        user.avatar,
            'servers':       servers
        }
        return self.respond(200, output)

    def get_server(self, event, id):
        # this looks dumb as we arent using the middleware
        # but this endpoint is used by users and the
        # discord bot... we also need the server id to check
        # if the user is an admin zzzzzzzzzzzz
        hbt = hasbottoken()
        if not hbt.is_bot(event) and not self.user_is_admin(event, id):
            return self.respond(403, "Forbidden")
        s = m_server.get(id)
        if not s:
            return self.respond(404, "Not Found")
        return self.respond(200, s.data)

    def set_server(self, event, id):
        if not self.user_is_admin(event, id):
            return self.respond(403, "Forbidden")
        s = m_server.get(id)
        if not s and 'name' in event['body'] and 'icon' in event['body']:
            s = m_server(id)
        s.update(event['body'])
        s.save()
        return self.respond(200, s.data)

    def join(self, event, id):
        s = m_server.get(id)
        if not s:
            s = m_server(id)
        s.join()
        s.save()
        return self.respond(200, "OK")

    def leave(self, event, id):
        s = m_server.get(id)
        if not s:
            s = m_server(id)
        s.leave()
        s.save()
        return self.respond(200, "OK")

    def user_is_admin(self, event, guild):
        try:
            return guild in event['logged_in_user'].admin_guilds
        except:
            pass
        return False
