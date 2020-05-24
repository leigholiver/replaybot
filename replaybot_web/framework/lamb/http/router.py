import json, importlib, re
from framework.lamb.http.rejection import rejection
from framework.lamb.http.response import response

class router():
    def __init__(self, routes, prefix):
        # inject a class prefix so that we can inject 
        # custom routes/controllers/middleware for testing
        self.routes = routes
        self.prefix = prefix

    def respond(self, event, context):
        try:
            if 'httpMethod' not in event.keys() or 'path' not in event.keys():
                return response(400, "Bad Request")

            # hack for cors checks
            if event['httpMethod'] == "OPTIONS":
                return response(200, "")

            if event['httpMethod'] in self.routes.keys():
                for route in self.routes[event['httpMethod']]:
                    match = re.search(route['path'], event['path'])
                    if (match):
                        route_params = match.groupdict()
                        route_params['event'] = event
                        controller, dot, function = route['action'].partition(".")
                        if 'middleware' in route.keys():
                            for mwname in route['middleware']:
                                mw = getattr(importlib.import_module(self.prefix + "middleware." + mwname), mwname)
                                mw = mw()
                                try:
                                    event = mw.process(event)
                                except rejection as e:
                                    return response(e.statusCode, e.body)
                        ctrlr = getattr(importlib.import_module(self.prefix + "controllers." + controller), controller)
                        ctrlr = ctrlr()
                        action = getattr(ctrlr, function)

                        if "body" in event.keys() and event['body'] != None:
                            try:
                                event['body'] = json.loads(event['body'])
                            except:
                                return response(400, "couldnt parse post body (json)")
                        result = action(**route_params)
                        return result
            return response(404, "Not Found")

        except Exception as e:
            raise e
            print(e)
            return response(500, "Internal Server Error")
