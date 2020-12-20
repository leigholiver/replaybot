import time, datetime
from framework.lamb.command import command
from support.discord import discord
from models.user import user
from models.server import server

class updatemeta(command):
    # dont update more than once every 10 mins
    max_update_freq_sec = 600

    user_batch_count   = 25
    server_batch_count = 25

    def run(self, data):
        disco = discord()

        cutoff = int(time.time()) if '--force' in data else (int(time.time()) - self.max_update_freq_sec)
        cutoff = datetime.datetime.fromtimestamp(cutoff).isoformat()

        # get the 25 oldest updated users
        # update the meta
        users = user.list(limit=self.user_batch_count, before=cutoff, direction="asc")

        for u in users:
            disco.update_user_meta(u)
            disco.update_user_guilds(u)
            u.save()

        # get the 25 oldest updated servers
        # update the meta
        servers = server.list(limit=self.server_batch_count, before=cutoff, direction="asc")
        for s in servers:
            disco.update_guild_meta(s)

        print("updated %d users and %d servers" % (len(users), len(servers)))
        return True
