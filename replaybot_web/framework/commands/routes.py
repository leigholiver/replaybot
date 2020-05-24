import os, json
from routes import routes as routes_input
from framework.util.route_util import route_util
from framework.lamb.command import command

class routes(command):
    routes_output = os.path.dirname(os.path.realpath(__file__)) + "/../../api/routes_compiled.py"
    edit_message = "this file is managed by lamb. any changes to it will be lost."

    def run(self, data):
        ru = route_util()
        output = ru.compile_routes(routes_input)
        with open(self.routes_output, 'w') as output_file:
            output_file.write('# ' + self.edit_message + '\nroutes = ' + json.dumps(output, indent=4, sort_keys=True))
        print("Routes compiled")
        return True
