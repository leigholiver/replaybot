import os
from support.lamb.Command import Command
from util.HashUtil import HashUtil

# pulls together the /api folder and the /packages folder
# ready to be zipped up by terraform
class gather(Command):
    def run(self, data):
        
        hasher = HashUtil()

        if hasher.hasChanged(os.getcwd() + "/api"):
            os.system('cp -r api/* deploy/build')
        else:
            print("No api update needed, skipping")        

        if hasher.hasChanged(os.getcwd() + "/packages.txt"):
            os.system('pip install -r packages.txt -t deploy/build')
        else:
            print("No packages update needed, skipping")