import os
from framework.lamb.command import command
from framework.util.hash_util import hash_util

# pulls together the /api folder and the /packages folder
# ready to be zipped up by terraform
class gather(command):
    def run(self, data):
        hasher = hash_util()
        api_path     = "api"
        support_path = "framework"
        build_dir    = ".build"

        print("Gathering...")

        # copy lamb support folder
        if hasher.has_changed(os.path.abspath(support_path)) or '-y' in data:
            os.system("mkdir -p " + build_dir + "/" + support_path + " && cp -r " + support_path + "/lamb " + build_dir + "/" + support_path)
        else:
            print("No support update needed, skipping")

        # copy api src
        if hasher.has_changed(os.path.abspath(api_path)) or '-y' in data:
            os.system("cp -r " + api_path + "/* " + build_dir)
        else:
            print("No api update needed, skipping")        

        # install packages
        if hasher.has_changed(os.path.abspath(api_path + "/packages.txt")) or '-y' in data:
            os.system("pip install -r " + api_path + "/packages.txt -t " + build_dir)
        else:
            print("No packages update needed, skipping")
        return True