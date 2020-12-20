handlers = [
    "api",
    "cron",
    "queue"
]

def lambda_handler(event, context):
    for handler in handlers:
        hdnlr = get_handler(handler)()
        if hdnlr.is_valid(event):
            return hdnlr.handle(event, context)

    return {
        'statusCode': 400,
        'body': '"Bad Request"'
    }
       
def get_handler(name):
    obj = None
    try:
        obj = getattr(__import__("framework.lamb.handlers." + name, fromlist=[None]), name)
    except ModuleNotFoundError as e:
        return False
    return obj