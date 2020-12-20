import os
from framework.lamb.controller import controller
from support.discord import discord as discord_util
from support.auth import auth as auth_util

class discord(controller):
    def exchange_code(self, event):
        auth  = auth_util()
        disco = discord_util()
        user = disco.handle_code(self.query(event, 'code'))
        if not user:
            return self.respond(400, "Bad Request")

        disco.update_user_guilds(user)
        user.save()
        token = auth.token(user.id)
        return self.respond(302, token, headers = {"Location": "%s?token=%s" % (os.getenv('FRONTEND_LOGIN_ENDPOINT'), token)})
