import json
from framework.lamb.handlers.handlerinterface import handlerinterface

class cron(handlerinterface):
    def is_valid(self, event):
        if isinstance(event, str):
            try:
                json.loads(event)
                return True
            except:
                pass
        return False

    def handle(self, event, context):
        data = []
        try:
            data = json.loads(event)
            if not isinstance(data, list):
                raise Exception

            cmd = data[0].lower()

            if cmd == "wool":
                print("🐑 wool is keeping your lamb warm 🐑")
                return {
                    'statusCode': 200,
                    'body': '"OK"'
                }
            
            # get the command object
            c = self.get_command_obj(cmd)

        except Exception as e:
            print("Cron boot time error: " + str(e))
            return {
                'statusCode': 400,
                'body': '"Bad Request"'
            }

        # instantiate and run the command
        try:
            c = c()
            c.run(data[1:])
        except Exception as e:
            print("Cron run time error: " + str(e))
            return {
                'statusCode': 500,
                'body': '"Internal Server Error"'
            }
        return {
            'statusCode': 200,
            'body': '"OK"'
        }

    def get_command_obj(self, name):
        obj = None
        try:
            obj = getattr(__import__("framework.tests.support.commands." + name, fromlist=[None]), name)
        except ModuleNotFoundError as e:
            obj = getattr(__import__("commands." + name, fromlist=[None]), name)
        return obj