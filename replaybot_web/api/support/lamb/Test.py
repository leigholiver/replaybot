import json
from router import router
from routes_compiled import routes

class colors:
    HEADER = '\033[94m'
    SKIP = '\033[95m'
    SUCCESS = '\033[92m'
    FAIL = '\033[91m'
    WARN = '\033[93m'
    END = '\033[0m'

class Test():
    successful = True
    name = ""
    router = router(routes, "")
    
    def run(self):
        return True

    def record(self, result, expected, response):
        if result: 
            self.success("Response: " + str(response))
        else:
            self.fail("Expected: " + str(expected))
            self.fail("Response: " + str(response))

    def getRequest(self, data):
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

    def postRequest(self, data, postData):
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
            "body": json.dumps(postData),
        }
        request.update(data)
        return self.router.respond(request, {})
    
    def header(self, message):
        print(colors.HEADER + "--[ " + message + " ] --" + colors.END)

    def warn(self, message):
        output = colors.SKIP + "[WARNING] "
        if message != "":
            output += message            
        output += colors.END
        print(output)

    def skip(self, message = ""):
        output = colors.SKIP + "[SKIPPING] "
        if message != "":
            output += message
            
        output += colors.END
        print(output)

    def success(self, message = ""):
        output = colors.SUCCESS + "[SUCCESS] "
        if message != "":
            output += message
            
        output += colors.END
        print(output)

    def fail(self, message = ""):
        self.successful = False
        output = colors.FAIL + "[FAIL] "
        if message != "":
            output += message
            
        output += colors.END
        print(output)