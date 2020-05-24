import json
from framework.lamb.http.router import router as _router
from framework.util.route_util import route_util
from routes import routes as routes_input

class colors:
    HEADER = '\033[94m'
    SKIP = '\033[95m'
    INFO = '\033[95m'
    SUCC = '\033[92m'
    FAIL = '\033[91m'
    WARN = '\033[93m'
    END = '\033[0m'

class test():
    successful = True
    name = ""

    r_util = route_util()
    routes = r_util.compile_routes(routes_input)
    router = _router(routes, "")
    
    def run(self):
        return True

    def record(self, result, expected, response):
        if result: 
            self.success("Response: " + str(response))
        else:
            self.fail("Expected: " + str(expected))
            self.fail("Response: " + str(response))

    def get_request(self, data):
        request = {
            "resource":"/{proxy+}",
            "path":"/get",
            "httpMethod":"GET",
            "headers":"null",
            "multiValueHeaders":"null",
            "queryStringParameters":"null",
            "multiValueQueryStringParameters":"null",
            "pathParameters":{"proxy":"ping"},
            "stageVariables":"null",
            "resourcePath":"/{proxy+}"
        }
        request.update(data)
        return self.router.respond(request, {})

    def post_request(self, data, post_data):
        request = {
            "resource":"/{proxy+}",
            "path":"/post",
            "httpMethod":"POST",
            "headers":"null",
            "multiValueHeaders":"null",
            "queryStringParameters":"null",
            "multiValueQueryStringParameters":"null",
            "pathParameters":{"proxy":"ping"},
            "stageVariables":"null",
            "resourcePath":"/{proxy+}",
            "Content-Type": [ "application/json" ],
            "body": json.dumps(post_data),
        }
        request.update(data)
        return self.router.respond(request, {})
    
    def header(self, message):
        self.message(colors.HEADER, "--[ " + message + " ] --")

    def warn(self, message):
        self.message(colors.WARN, "[WARN] " + message)
    
    def skip(self, message = ""):
        self.message(colors.SKIP, "[SKIP] " + message)

    def info(self, message = ""):
        self.message(colors.SKIP, "[INFO] " + message)

    def success(self, message = ""):
        self.message(colors.SUCC, "[SUCC] " + message)

    def fail(self, message = ""):
        self.message(colors.FAIL, "[FAIL] " + message)
        self.successful = False

    def message(self, colour, message):
        print(colour + message + colors.END)