import os, json, subprocess
from framework.lamb.command import command

class dev(command):
    commands = [
        # dev api server
        "LAMB_ENV=local FLASK_APP=framework/dev_server.py FLASK_ENV=development python3 -m flask run",
        # queue worker
        "./lambctl work"
    ]
    
    def run(self, data):
        # run the flask server
        # os.system(self.command)
        procs = []
        for cmd in self.commands:
            procs.append(subprocess.Popen(cmd, shell=True))
        
        for proc in procs:
            try:
                proc.communicate()
            except KeyboardInterrupt:
                print("exiting...")
        
        return True