from framework.lamb.handlers.lambda_handler import lambda_handler as lamb_lambda

def lambda_handler(event, context):
    return lamb_lambda(event, context)