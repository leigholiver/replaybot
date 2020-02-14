import json

class Controller():
    def respond(self, status, body):
        return {
            'statusCode': status,
            'body': json.dumps(body),
            'headers': {
                'Content-Type': 'application/json', 
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST, GET, OPTIONS'
            }
        }

    def query(self, event, param):
        if isinstance(event['queryStringParameters'], dict) and param in event['queryStringParameters'].keys():
            return event['queryStringParameters'][param]
        return False