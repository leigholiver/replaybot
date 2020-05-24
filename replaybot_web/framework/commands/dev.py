import os, json
from framework.lamb.command import command

class dev(command):
    command = "LAMB_ENV=local FLASK_APP=framework/dev_server.py FLASK_ENV=development python3 -m flask run"
    
    def run(self, data):
        # run the flask server
        os.system(self.command)