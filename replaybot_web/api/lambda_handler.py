from framework.lamb.http.lambda_handler import lambda_handler as lamb_lambda

def lambda_handler(event, context):
    return lamb_lambda(event, context)