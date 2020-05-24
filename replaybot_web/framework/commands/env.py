import os, json
from framework.lamb.command import command
from framework.util.env_util import env_util

class env(command):
    output_dir = "environment/deployments/"

    def __init__(self):
        self.e_util = env_util()
        self.full   = self.e_util.get_full()

    def run(self, data):
        if not self.full:
            print("error: couldn't get environment")
            return False

        # create a new environments/environment.json file
        if len(data) == 1 and data[0] == "create":
            return self.create_environment_json(data)
        
        # verify the environment definitions
        if "verify" in data:
            result = self.e_util.verify_environments()
            if not result:
                print("invalid environments, aborting")
                return False

        # export the env.auto.tfvars.json file
        if "export" in data:
            result = self.e_util.export_tf_vars()
            if not result:
                print("couldn't export terraform vars file, aborting")
                return False

        # switch terraform workspace
        if "tfworkspace" in data:
            env_name = self.full['tf_workspace'] if "tf_workspace" in self.full.keys() else self.full['env_name']
            os.system("terraform workspace select " + env_name + " || terraform workspace new " + env_name)
        
        return self.full if "return-env" in data else True

    def create_environment_json(self, data):
        name             = input("environment name?: ")
        domain_name      = input("domain name? (example.com): ")
        branch_specifier = input("git branch specifier?: ")

        if name != "" and domain_name != "" and branch_specifier != "":
            output_file = self.output_dir + name + ".json"
            if os.path.isfile(output_file):
                print("error: environment file already exists")
                return False
            try:
                with open(output_file, "w") as file:
                    file.write(json.dumps({
                        "env_name": name,
                        "domain_name": domain_name,
                        "branch_specifier": branch_specifier
                    }, indent=4, sort_keys=True))
                print("environment created in " + output_file)
            except:
                print("error writing environment file")
                return False
        else:
            print("missing required information")
            return False
        return True