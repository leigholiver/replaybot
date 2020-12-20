import time, json, importlib, traceback
from framework.lamb.handlers.handlerinterface import handlerinterface
from framework.lamb.http.router import router
from routes_compiled import routes

class api(handlerinterface):
    def is_valid(self, event):
        if isinstance(event, dict) and "path" in event.keys() and "httpMethod" in event.keys():
            return True
        return False

    def handle(self, event, context):
        try:
            t_start = time.time()
            r = router(routes, "")
            t_boot = time.time()
            response = r.respond(event, context)
            t_response = time.time()

            log = {
                'time': event['requestContext']['requestTime'],
                'sourceIp': event['requestContext']['identity']['sourceIp'],
                'userAgent': event['requestContext']['identity']['userAgent'],
                'httpMethod': event['httpMethod'],
                'path': event['path'],
                'code': response['statusCode'],
                'boot': (t_boot - t_start) * 1000, # ms to s
                'response': (t_response - t_boot) * 1000, # ms to s
                'total': (t_response - t_start) * 1000 # ms to s
            }
            print(log)
            print(response)
            return response
        except Exception as e:
            print("API Exception: [%s] %s" % (e.__class__.__name__, str(e)))
            print(traceback.format_exc())
            return {
                'statusCode': 500,
                'body': '"Internal Server Error"'
            }
