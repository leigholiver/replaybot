import os
from framework.lamb.command import command
from framework.commands.dev import dev as lamb_dev

# override the default lamb dev server to also start the frontend
class dev(command):
    def run(self, data):
        environment  = " REACT_APP_API_URL=http://localhost:5000/api "
        environment += " REACT_APP_REDIRECT_URI=http://localhost:5000/api/discord "
        environment += " REACT_APP_CLIENT_ID="+os.getenv('CLIENT_ID')
        environment += " REACT_APP_DISCORD_INVITE="+os.getenv('DISCORD_INVITE')
        environment += " REACT_APP_DISCORD_SERVERID="+os.getenv('DISCORD_SERVERID')
        environment += " REACT_APP_IGNORE_HTTPS=true "
        environment += " BROWSER=none "

        dev_server = lamb_dev()
        dev_server.commands.append("cd frontend && " + environment + " yarn start")
        dev_server.run(data)