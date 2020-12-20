import json
from framework.lamb.http.response import response

class controller():

    def respond(self, code = None, message = None, headers = {}):
        return response(code, message, headers)

    # utility function for getting query string parameters
    def query(self, event, param):
        if isinstance(event['queryStringParameters'], dict) and param in event['queryStringParameters'].keys():
            return event['queryStringParameters'][param]
        return False

    def query_list(self, event, param):
        print(event)
        if ('multiValueQueryStringParameters' in event.keys() and 
                isinstance(event['multiValueQueryStringParameters'], dict) and 
                param in event['multiValueQueryStringParameters'].keys()):
            return event['multiValueQueryStringParameters'][param]
        return False

    # utility function for getting headers
    def header(self, header, event):
        if isinstance(event['headers'], dict) and header in event["headers"].keys():
            return event['headers'][header]
        return False