import os, pkgutil, inspect, lamb, json, re
from markdown2 import Markdown
from routes import routes
from support.lamb.Command import Command
from support.lamb.Model import Model
from util.templater.Templater import Templater

class make(Command):
    templater = Templater()
    
    # output folder for entities
    output_folder = os.path.dirname(os.path.realpath(__file__)) + "/../api/"
    
    # key is the template name, value is the output folder
    map = {
        'controller': 'controllers',
        'middleware': 'middleware',
        'command': '../commands',
        'model': 'models',
        'test': '../tests'
    }

    # specific file outputs
    # compiled routes
    routes_output = os.path.dirname(os.path.realpath(__file__)) + "/../api/routes_compiled.py"

    
    def run(self, data):
        # create the /main.tf deployment file
        if len(data) == 1 and ( data[0] == 'terraform' or data[0] == 'tf'):
            print("Generating Terraform...")
            self.makeTerraform()
        
        # build the routes cache
        elif len(data) == 1 and data[0] == 'routes':
            print("Processing routes...")
            self.compileRoutes()
            
        # Create entities
        elif len(data) == 2 and data[0] != "" and data[1] != "":
            if data[0] in self.map.keys():          
                type, name = data
                filename = self.output_folder + self.map[type] + "/" + name + ".py"
                try:
                    if not os.path.exists(filename):
                        self.templater.write(type + ".py.j2", filename, { 'name': name })
                        print(type + " " + name + " created!")
                    else:
                        print(type + " " + name + " already exists!")
                except Exception as e:
                    print("Sorry, there was an error creating the " + type)
                    raise e
            else:
                print("Sorry, I don't know how to make a " + data[0])
        else:
            print("Please specify something to make, and a name, eg")
            print("./lambctl make controller NewController")

    def scanForTables(self):
        table_names = []
        imported_package = __import__("models", fromlist=['blah'])
        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                try:
                    plugin_module = __import__(pluginname, fromlist=['blah'])
                    clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                    for (_, c) in clsmembers:
                        if issubclass(c, Model) & (c is not Model):
                            model = c()
                            table_names.append({ 'name': model.table, 'indexes': model.indexes, 'sort_key': model.sort_key })
                except Exception as e:
                    print(e)
                    pass
        return table_names

    def compileRoutes(self):
        output = {}        
        for route in routes.keys():
            obj = {
                "path": self.compile(route),
                "action": routes[route]['action'],
                "middleware": routes[route]['middleware']
            }

            for method in routes[route]['methods']:
                if method in output.keys():
                    output[method].append(obj)
                else:
                    output[method] = [obj]
        with open(self.routes_output, 'w') as output_file:
            output_file.write('# this file is managed by lamb. any changes to it will be lost.\nroutes = ' + json.dumps(output, indent=4, sort_keys=True))


    def compile(self, route):
        tmp = route.replace("/", "\\/")
        tmp = tmp.replace("(", "(?P<")
        tmp = tmp.replace(")", ">.*?)")
        if not tmp.endswith("/"):
            tmp += "\\/?"   
        tmp += "$"
        return tmp


    def makeTerraform(self):
        files = {
            'platform': {
                'dir': os.path.dirname(os.path.realpath(__file__)) + "/../",
                'data': { 'lamb': lamb }
            },
            'db': {
                'dir': os.path.dirname(os.path.realpath(__file__)) + "/../deploy/db/",
                'data': { 'tables': self.scanForTables() }
            },
            'api': {
                'dir': os.path.dirname(os.path.realpath(__file__)) + "/../deploy/api/",
                'data': { }
            },
            'public': {
                'dir': os.path.dirname(os.path.realpath(__file__)) + "/../deploy/public/",
                'data': { 'no_www': lamb.no_www }
            }
        }

        edit_message = """# this file is managed by lamb, any changes to it will be lost
# edit 'main.tf.j2' and run'./lambctl make terraform' to regenerate it"""
        
        for key in files.keys():
            files[key]['data']['edit_message'] = edit_message
            self.templater.write(files[key]['dir'] + "main.tf.j2", files[key]['dir'] + "main.tf", files[key]['data'])