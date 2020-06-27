import sys, os, json, mpyq, requests, uuid, datetime
from flask import Flask, Response, request
from parser import parse_replay

app = Flask(__name__)

@app.route('/ping', methods=["GET"])
def ping():
    return "pong"

@app.route('/', methods=["POST"])
def parse():
    filename = "/tmp/" + str(uuid.uuid4())
    content = request.json

    try:
        url = content['url']
    except:
        return Response(400)

    try:
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
            f.close()

        output = parse_replay(filename)
        if not output:
            return Response(500)
        print(output)
        return Response(response=json.dumps(output),
                    status=200,
                    mimetype="application/json")
    except:
        return Response(500)

    return Response(400)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')