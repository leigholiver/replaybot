import sys, os, json
from framework.lamb.command import command
from framework.util.runner import runner

class deploy(command):
    tf_state_config_path = "environment/state.tfvars"

    def run(self, data):
        runboy = runner()

        try:
            with open('secrets.env') as f:
                os.environ.update(
                    line.replace('export ', '', 1).strip().split('=', 1) for line in f
                    if 'export' in line
                )
        except:
            print("couldnt get secrets, aborting")
            return False

        # Generate env.auto.tfvars.json for terraform
        environment = runboy.run(["env", "verify", "export", "return-env"])
        if environment == False or 'domain_name' not in environment.keys():
            print(environment['domain_name'])
            print("No environment detected, aborting")
            return False

        # run the pre deploy tasks
        pre_tasks = [
            ["routes"]
        ]
        if 'pre_deploy_tasks' in environment.keys():
            pre_tasks = environment['pre_deploy_tasks'] + pre_tasks
        results = runboy.multi_run(pre_tasks)
        for result in results:
            if not result:
                print("pre deploy tasks failed, aborting")
                return False

        # run ze tests
        if '--skip-tests' not in data and "deploy_tests" in environment.keys():
            deploy_tests = environment["deploy_tests"]
            deploy_tests.insert(0, "tests")
            result = runboy.run(deploy_tests)
            if not result and '--ignore-tests' not in data:
                print("Tests failed, aborting")
                return False

        # run the deployment via terraform
        result = os.system('terraform init -backend-config=' + self.tf_state_config_path)
        if result != 0:
            print("terraform init failed, aborting")
            return False

        # has to be run after terraform init
        result = runboy.run(["env", "tfworkspace"])
        if not result:
            print("`./lambctl env tfworkspace` failed, aborting")
            return False

        if '-auto-approve' in data or '-y' in data:
            result = os.system('terraform apply -auto-approve')
            if result != 0:
                print("terraform apply failed, aborting")
                return False
        else:
            result = os.system('terraform apply')
            if result != 0:
                print("terraform apply failed, aborting")
                return False

        # run the post deploy tasks
        if 'post_deploy_tasks' in environment.keys():
            results = runboy.multi_run(environment['post_deploy_tasks'])
            for result in results:
                if not result:
                    print("post deploy tasks failed, aborting")
                    return False
        return True
