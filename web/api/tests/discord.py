import os, json, urllib.parse
from framework.lamb.test import test
from support.auth import auth as auth_util
from support.discord import discord as discord_util
from models.server import server

class discord(test):
    name = "discord"

    def run(self):
        self.header("discord code test")
        if not os.getenv('CI'):
            test_user_id = input("discord user id: ")
            if test_user_id == "":
                test_user_id = "95462775685394432"

            print("please go to this url in your browser, and once authorized and redirected, enter the code= parameter from the url")
            print("https://discord.com/api/oauth2/authorize?client_id=" + os.getenv('CLIENT_ID') + "&redirect_uri=" + urllib.parse.quote(os.getenv("REDIRECT_URI"), safe='') + "&response_type=code&scope=identify%20guilds")
            code = input("code=")

            rsp = self.get_request({
                "path":"/discord",
                "queryStringParameters": {
                    "code": code
                }
            })
            token = json.loads(rsp['body'])
            au = auth_util()
            result = au.verify_token(token, test_user_id)
            self.record(result, "Success and valid token", "Success and valid token" if result else "Success but invalid token")
        else:
            self.skip("cannot run discord test in CI, skipping")

        self.header("channel visibility test")
        SERVER_ID          = "569854781032759296"  # id of the server
        PRIVATE_CHANNEL_ID = "718851198471635064"  # id of a private channel in the server
        PUBLIC_CHANNEL_ID  = "675514092689293313"  # id of a public channel in the server
        PRIVILEGED_ACCOUNT = "95462775685394432"   # account id with visibility of private channel
        LIMITED_ACCOUNT    = "675701018301825044"  # account id with no visibility of private channel

        # refresh the meta
        disco = discord_util()
        result = disco.update_guild_meta_by_id(SERVER_ID)
        print("update guild meta result: %s" % "Success" if result else "Fail")

        # grab the server
        s = server.get(SERVER_ID)

        # test
        priv_can_see_private = disco.user_can_see_channel(s, PRIVILEGED_ACCOUNT, PRIVATE_CHANNEL_ID)
        pleb_can_see_private = disco.user_can_see_channel(s, LIMITED_ACCOUNT, PRIVATE_CHANNEL_ID)
        priv_can_see_public = disco.user_can_see_channel(s, PRIVILEGED_ACCOUNT, PUBLIC_CHANNEL_ID)
        pleb_can_see_public = disco.user_can_see_channel(s, LIMITED_ACCOUNT, PUBLIC_CHANNEL_ID)

        print("i can see private channel?: %s" % str(priv_can_see_private))
        print("test account can see private channel?: %s" % str(pleb_can_see_private))
        print("i can see public channel?: %s" % str(priv_can_see_public))
        print("test account can see public channel?: %s" % str(pleb_can_see_public))

        result = (
            priv_can_see_private and
            not pleb_can_see_private and
            priv_can_see_public and
            pleb_can_see_public
        )

        self.record(result, "True", result)
        return self.successful
