import time, json, importlib
from framework.lamb.http.router import router
from routes_compiled import routes

def lambda_handler(event, context):
    if is_api_request(event):
        return handle_api_request(event, context)
    elif is_cron(event):
        return handle_cron(event, context)

    return {
        'statusCode': 400,
        'body': '"Bad Request"'
    }

def is_api_request(event):
    if isinstance(event, dict) and "path" in event.keys() and "httpMethod" in event.keys():
        return True
    return False

def is_cron(event):
    if isinstance(event, str):
        try:
            json.loads(event)
            return True
        except:
            pass
    return False

def handle_api_request(event, context):
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
        return response
    except Exception as e:
        print(event)
        print(e)
        return {
            'statusCode': 500,
            'body': '"Internal Server Error"'
        }
        
def handle_cron(event, context):
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
        c = get_command_obj(cmd)

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

def get_command_obj(name):
    obj = None
    try:
        obj = getattr(__import__("framework.tests.support.commands." + name, fromlist=[None]), name)
    except ModuleNotFoundError as e:
        obj = getattr(__import__("commands." + name, fromlist=[None]), name)
    return obj