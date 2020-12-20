import os
from routes import routes
from framework.lamb.command import command
from framework.util.templater import templater

class make(command):
    tpmltr = templater()
    
    # output folder for entities
    output_folder = os.path.dirname(os.path.realpath(__file__)) + "/../../api"
    
    # key is the template name, value is the output folder relative to output_folder
    map = {
        'controller': '/controllers',
        'middleware': '/middleware',
        'command': '/commands',
        'model': '/models',
        'test': '/tests'
    }
    
    def run(self, data):
        if len(data) == 2 and data[0] != "" and data[1] != "":
            if data[0] in self.map.keys():          
                type, name = data
                filename = self.output_folder + self.map[type] + "/" + name + ".py"
                try:
                    if not os.path.exists(filename):
                        self.tpmltr.write(type + ".py.j2", filename, { 'name': name })
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
            print("./lambctl make controller new_controller")