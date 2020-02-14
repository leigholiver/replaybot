import lamb, os, sys
from support.lamb.Command import Command
from commands.build import build

class deployui(Command):
    def run(self, data):
        builder = build()
        result = builder.run([])
        if not result:
            print("Build failed, aborting")
            sys.exit(1)

        os.system("aws s3 sync --delete --acl public-read ui/build s3://" + ("www." if not lamb.no_www else "") + "$TF_VAR_domain_name")