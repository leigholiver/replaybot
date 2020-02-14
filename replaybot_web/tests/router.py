from support.lamb.Test import Test
from router import router as app_router
from tests.support.routes import routes

class router(Test):
    name = "router"
    def run(self):
        self.router = app_router(routes, "tests.support.")

        # ping test
        self.header("ping test")
        rsp = self.getRequest({
            "path":"/ping"
        })
        expected = {'statusCode': 200, 'body': '"pong"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"pong"'
        self.record(result, expected, rsp)

        # 404 not found test
        self.header("404 not found test")
        rsp = self.getRequest({
            "path":"/sdtstsdtasdtasdkfjasidfasdf-doesnt-exist-zzzzzzzz"
        })
        expected = {'statusCode': 404, 'body': '"Not Found"'}
        result = rsp == expected
        self.record(result, expected, rsp)


        # middleware injection test
        self.header("middleware injection test")
        rsp = self.getRequest({
            "path":"/pong"
        })
        result = rsp['statusCode'] == 200 and "MiddlewareInjected" in rsp['body']
        expected = str("rsp['statusCode'] == 200 and \"\"MiddlewareInjected\"\" in rsp['body']")
        self.record(result, expected, rsp)


        # middleware reject test
        self.header("middleware reject test")
        rsp = self.getRequest({
            "path":"/pong",
            "queryStringParameters": { 'reject': 1 }
        })
        expected = {'statusCode': 403, 'body': '"Forbidden"'}
        result = rsp == expected
        self.record(result, expected, rsp)


        # middleware custom reject test
        self.header("middleware reject test")
        rsp = self.getRequest({
            "path":"/pong",
            "queryStringParameters": { 'teapot': 1 }
        })
        expected = {'statusCode': 418, 'body': '"I\'m a teapot"'}
        result = rsp == expected
        self.record(result, expected, rsp)
    

        # post ping test
        self.header("POST ping test")
        rsp = self.postRequest({
            "path":"/ping"
        }, {})
        expected = {'statusCode': 200, 'body': '"pong"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"pong"'
        self.record(result, expected, rsp)

        # route parameters test
        self.header("route parameters test")
        rsp = self.getRequest({
            "path":"/hello/john"
        })
        expected = {'statusCode': 200, 'body': '"hello, john"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"hello, john"'
        self.record(result, expected, rsp)

        return self.successful