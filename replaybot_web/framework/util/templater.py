import os
from jinja2 import Template

class templater():
    templates_folder = os.path.dirname(os.path.realpath(__file__)) + "/templates/"

    def write(self, template, outputFile, params):
        
        if os.path.isfile(self.templates_folder + template):
            tmp = self.templates_folder + template
        elif os.path.isfile(template):
            tmp = template
        else:
            return False

        with open(tmp, 'r') as file:
            data = file.read()
            t = Template(data)
            output = t.render(params)
            with open(outputFile, "w") as file:
                file.write(output)
