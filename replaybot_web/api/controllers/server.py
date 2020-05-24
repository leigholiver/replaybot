from framework.lamb.controller import controller
from models.server import server as m_server
from models.replay import replay
from controllers.discord import discord
from middleware.hasbottoken import hasbottoken

class server(controller):
    def get_server_joined(self, event, id):
        s = m_server.get(id)
        if not s:
            return self.respond(404, "Server Not Found")
        return self.respond(200, s.joined)

    def get_server(self, event, id):
        hbt = hasbottoken()
        is_bot = hbt.is_bot(event)

        if not is_bot and not self.user_is_admin(event, id):
            return self.respond(403, "Forbidden")

        s = m_server.get(id)
        if not s:
            return self.respond(404, "Not Found")
        return self.respond(200, s.data)

    def set_server(self, event, id):
        if not self.user_is_admin(event, id):
            return self.respond(403, "Forbidden")

        s = m_server.get(id)

        # allow metadata post to create
        if not s and 'name' in event['body'] and 'icon' in event['body']:
            s = m_server(id)

        s.update(event['body'])
        s.save()
        return self.respond(200, s.data)

    def store_replay(self, event, id):
        rep = replay(id, event['body'])
        rep.save()
        return self.respond(200, "OK")

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
        header = self.header("Authorization", event)
        if not header:
            header = self.header("authorization", event)
        if not header:
            return False
        
        disco = discord()        
        if not disco.user_is_admin(guild, header):
            return False
        return True