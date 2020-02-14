import os
from support.lamb.Command import Command
from util.HashUtil import HashUtil

class build(Command):
    def run(self, data):

        # set api_url
        os.system("echo \"module.exports = { \n\
    clientID: \\\"$TF_VAR_CLIENT_ID\\\", \n\
    redirectURI: \\\"https://$TF_VAR_domain_name/discord\\\", \n\
    apiURL: \\\"https://$TF_VAR_domain_name/$TF_VAR_api_path\\\" \n\
}\" > ui/src/api.js");

        hasher = HashUtil()
        if hasher.hasChanged(os.getcwd() + "/ui", [ "/ui/node_modules", "/ui/build" ]) or '-y' in data:          
            # switch to ui folder
            os.chdir("ui")

            # build
            result = os.system('yarn build')
            if result != 0:
                return False
                
            os.chdir("..")
        else:
            print("No /ui update needed, skipping")
        
        return True