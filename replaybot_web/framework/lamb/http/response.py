import json

def response(code, content):
    return {
        'statusCode': code,
        'body': json.dumps(content), 
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
            'Access-Control-Allow-Headers': '*'
        }
    }