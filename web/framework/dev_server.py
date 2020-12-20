import sys, os, re, json
from flask import Flask, request, Response, redirect, send_from_directory
from framework.util.env_util import env_util
from framework.lamb.http.router import router as _router
from framework.util.route_util import route_util

# add api folder to path
sys.path.insert(0,os.path.dirname(os.path.realpath(__file__)) + "/../api")
from routes import routes as routes_input

e_util = env_util()
r_util = route_util()
router = _router(r_util.compile_routes(routes_input), "")
app = Flask(__name__, static_folder=None)

@app.route('/', defaults={'u_path': ''}, methods = ['GET', 'POST'])
@app.route('/<path:u_path>', methods = ['GET', 'POST'])
def catch_all(u_path):
    # gross
    path = "/" + u_path

    # api requests
    api_request_path = matches_path("api", path)
    if api_request_path:
        # dynamically set routes/env vars
        setup_env_vars()
        router.routes = r_util.compile_routes(routes_input)
        response = router.respond(process_request(api_request_path, request), {})
        resp = process_response(response)
        return resp

    # bucket requests
    env = e_util.get_tf_vars()
    if env and 'buckets' in env.keys():
        root_bucket = None
        for bucket in env['buckets']:
            if bucket['subdomain'] != "":
                bucket_path = matches_path(bucket['subdomain'], path)
                if bucket_path != False:
                    return from_bucket(request, bucket, bucket_path)
            else:
                root_bucket = bucket
        # want to do this after we've checked the api and any other buckets
        if root_bucket:
            return from_bucket(request, root_bucket, path)
    return Response(status=404, response="Not Found")

def setup_env_vars():
    env_vars = e_util.get_full()
    e_util.process_secrets(env_vars)
    os.environ.update(env_vars['api_config']['env_vars'])

def from_bucket(request, bucket, bucket_path):
    if bucket_path == "" or bucket_path == "/":
        bucket_path = "/index.html"
    # react router compatibility
    if not os.path.isfile(os.path.abspath(bucket['content_dir']) + "/" + bucket_path[1:]) and bucket['use_react_router'] != "":
        return redirect(request.host_url + bucket['subdomain'] + "/#!" + bucket_path)
    return send_from_directory(os.path.abspath(bucket['content_dir']), bucket_path[1:])

def matches_path(stage, path):
    result = re.search("\/" + stage + "($|\/$|(\/.*))", path)
    if result == None:
        return False
    return result.group(1)

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = 'POST, GET, OPTIONS'
    response.headers["Access-Control-Allow-Headers"] = '*'
    return response

# take the flask request object, turn it into a lamb api gateway request
def process_request(path, request):
    try:
        data = json.dumps(request.get_json(force=True))
    except:
        data = None

    # lowercase the headers, for some reason
    # flask uppercases the first character?
    headers = {}
    for key in dict(request.headers).keys():
        headers[key.lower()] = request.headers[key]

    return {
        "httpMethod": request.method,
        "path": path,
        "headers": headers,
        "queryStringParameters": dict(request.args),
        "multiValueQueryStringParameters": request.args.to_dict(flat=False),
        "body": data
    }

# take the lamb response and convert it to a flask response
def process_response(response):
    return Response(
        response     = response['body'] if 'body' in response.keys() else "",
        status       = response['statusCode'],
        headers      = response['headers'],
        content_type = "application/json",
    )
