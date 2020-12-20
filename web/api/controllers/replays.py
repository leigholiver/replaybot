from framework.lamb.controller import controller
from framework.lamb.queue.queue_util import queue_util
from support.discord import discord as discord_util
from support.indexer import indexer
from models.replay import replay

class replays(controller):
    def get_channels(self, event):
        disco            = discord_util()
        visible_channels = disco.get_user_visible_channels(event['logged_in_user'])
        req_channels     = self.query_list(event, 'channels')
        output           = []
      
        if not req_channels:
            return visible_channels

        for channel in req_channels:
            if channel in visible_channels:
                output.append(channel)

        return output

    def list(self, event):
        channels = self.get_channels(event)
        guild    = self.query(event, 'guild')
        cursor   = self.query(event, 'cursor') if self.query(event, 'cursor') else 0
        try:
            idx = indexer()
            result = idx.list(channels, guild, cursor)
            if not result:
                return self.respond(500, "Internal Server Error")
            return self.respond(200, result)
        except Exception as e:
            print(e)
            return self.respond(500, "Internal Server Error")
        return self.respond(400, "Bad Request")

    def search(self, event):
        channels = self.get_channels(event)
        cursor   = self.query(event, 'cursor') if self.query(event, 'cursor') else 0
        guild    = self.query(event, 'guild')
        query    = self.query(event, 'query')
        if not query:
            return self.respond(400, "Bad Request")
       
        try:
            idx = indexer()
            result = idx.search(channels, query, guild, cursor)
            if not result:
                return self.respond(500, "Internal Server Error")
            return self.respond(200, result)
        except Exception as e:
            print(e)
        
        return self.respond(500, "Internal Server Error")

    def store(self, event):
        rep = replay(event['body']['source']['guild']['id'], event['body'])
        rep.save()
        qu = queue_util()
        qu.enqueue({
            'class': 'support.indexer',
            'function': 'index_from_data',
            'kwargs': {
                'replay_data': rep.data
            }
        })
        return self.respond(200, "OK")