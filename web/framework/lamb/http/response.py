import json

default_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': '*'
}

def response(code, content, headers = {}):
    tmp = dict(default_headers)
    tmp.update(headers)
    print(content)
    return {
        'statusCode': code,
        'body': json.dumps(content),
        'headers': tmp
    }
