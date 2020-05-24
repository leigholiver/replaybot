import json
from framework.lamb.http.response import response

class controller():

    def respond(self, code = None, message = None):
        return response(code, message)

    # utility function for getting query string parameters
    def query(self, event, param):
        if isinstance(event['queryStringParameters'], dict) and param in event['queryStringParameters'].keys():
            return event['queryStringParameters'][param]
        return False

    # utility function for getting headers
    def header(self, header, event):
        if isinstance(event['headers'], dict) and header in event["headers"].keys():
            return event['headers'][header]
        return False