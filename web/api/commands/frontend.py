import os
from framework.lamb.command import command
from framework.util.hash_util import hash_util
from framework.util.env_util import env_util

class frontend(command):
    def run(self, data):
        hasher   = hash_util()
        e_util   = env_util()
        env      = e_util.get_full()
        env_name = e_util.get_name(True)

        api_url      = os.getenv("API_URL")
        redirect_uri = os.getenv("REDIRECT_URI")
        client_id    = os.getenv('PRODUCTION_CLIENT_ID') if env_name == "master" else os.getenv('CLIENT_ID')
        ga_id        = os.getenv("GA_ID")
        discord_serverid = os.getenv("DISCORD_SERVERID")
        discord_invite   = os.getenv("DISCORD_INVITE")

        print("using api_url: %s, redirect_uri: %s" % (api_url, redirect_uri))

        dir_changed     = hasher.has_changed(os.getcwd() + "/frontend", [ "/frontend/node_modules", "/frontend/build" ])
        api_url_changed = hasher.key_changed('api_url', api_url)
        redirect_uri_changed = hasher.key_changed('redirect_uri', redirect_uri)
        client_id_changed = hasher.key_changed('client_id', client_id)

        if dir_changed or api_url_changed or redirect_uri_changed or client_id_changed or '-y' in data:
            environment  = " REACT_APP_API_URL=" + api_url
            environment += " REACT_APP_REDIRECT_URI=" + redirect_uri
            environment += " REACT_APP_CLIENT_ID=" + client_id

            if discord_serverid and discord_invite:
                environment += " REACT_APP_DISCORD_SERVERID=" + discord_serverid
                environment += " REACT_APP_DISCORD_INVITE=" + discord_invite

            if ga_id:
                environment += " REACT_APP_GA_ID=" + ga_id

            os.chdir("frontend")
            result = os.system(environment + ' yarn build')
            os.chdir("..")
            if result != 0:
                return False
        else:
            print("no /frontend build needed, skipping")
        return True
