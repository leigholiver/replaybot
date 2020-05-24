import os,subprocess
from framework.lamb.command import command
from framework.commands.dev import dev as lamb_dev

# override the default lamb dev server to also start the frontend
class dev(command):
    def run(self, data):
        environment  = " REACT_APP_API_URL=http://localhost:5000/api "
        environment += " REACT_APP_REDIRECT_URI=http://localhost:3000/discord "
        environment += " REACT_APP_CLIENT_ID="+os.getenv('CLIENT_ID')
        environment += " REACT_APP_IGNORE_HTTPS=true "

        # start the dev servers
        dev   = subprocess.Popen(lamb_dev().command, shell=True)
        react = subprocess.Popen("cd frontend && " + environment + " yarn start", shell=True)
        
        # wait for them to finish or w/e
        try:
            dev.communicate()
            react.communicate()
        except KeyboardInterrupt:
            print("exiting...")