import sys, os, lamb
from support.lamb.Command import Command
from commands.make import make
from commands.tests import tests
from commands.deployui import deployui
from commands.gather import gather

class deploy(Command):
    def run(self, data):
        maker = make()
        maker.run(['terraform'])
        maker.run(['routes'])
        
        if '--skip-tests' not in data:
            tester = tests()
            result = tester.run(lamb.deploy_tests)
            if not result and '--ignore-tests' not in data:
                print("Tests failed, aborting")
                sys.exit(1)

        gatherer = gather()
        gatherer.run([])

        os.system('terraform init')

        if '-auto-approve' in data or '-y' in data:
            os.system('terraform apply -auto-approve')
        else:
            os.system('terraform apply')
        
        if '--skip-ui' not in data:
            builder = deployui()
            builder.run([])