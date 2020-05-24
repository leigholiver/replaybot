import os, json
from framework.util.env_util import env_util

class runner():
    def multi_run(self, tasks):
        results = []
        for task in tasks:
            try:
                result = self.run(task)
            except Exception as e:
                print("error running task [" + json.dumps(task) + "]: " + str(e))
                result = False
            results.append(result)
        return results

    def run(self, args):
        success = env_util().setup_env(args)
        if not success:
            print("no environment detected, aborting")
            return False

        # todo: runner prioritises api commands over framework commands, probably correct but is it?
        try:
            cmd = args[0].lower()
            c = getattr(__import__("commands." + cmd, fromlist=[""]), cmd)
        except ModuleNotFoundError as e:
            try:
                c = getattr(__import__("framework.commands." + cmd, fromlist=[""]), cmd)
            except ModuleNotFoundError as e:
                print(e)
                print("Unknown Command")
                return False

        c = c()
        return c.run(args[1:])