from framework.lamb.test import test
from framework.lamb.http.router import router as app_router
from framework.tests.support.routes import routes

class router(test):
    name = "router"
    def run(self):
        self.router = app_router(routes, "framework.tests.support.")

        # ping test
        self.header("ping test")
        rsp = self.get_request({
            "path":"/ping"
        })
        expected = {'statusCode': 200, 'body': '"pong"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"pong"'
        self.record(result, expected, rsp)

        # 404 not found test
        self.header("404 not found test")
        rsp = self.get_request({
            "path":"/sdtstsdtasdtasdkfjasidfasdf-doesnt-exist-zzzzzzzz"
        })
        expected = {'statusCode': 404, 'body': '"Not Found"'}
        result = rsp['statusCode'] == 404 and rsp['body'] == '"Not Found"'
        self.record(result, expected, rsp)


        # middleware injection test
        self.header("middleware injection test")
        rsp = self.get_request({
            "path":"/pong"
        })
        result = rsp['statusCode'] == 200 and "MiddlewareInjected" in rsp['body']
        expected = str("rsp['statusCode'] == 200 and \"\"MiddlewareInjected\"\" in rsp['body']")
        self.record(result, expected, rsp)


        # middleware reject test
        self.header("middleware reject test")
        rsp = self.get_request({
            "path":"/pong",
            "queryStringParameters": { 'reject': 1 }
        })
        expected = {'statusCode': 403, 'body': '"Forbidden"'}
        result = rsp['statusCode'] == 403 and rsp['body'] == '"Forbidden"'
        self.record(result, expected, rsp)


        # middleware custom reject test
        self.header("middleware reject test")
        rsp = self.get_request({
            "path":"/pong",
            "queryStringParameters": { 'teapot': 1 }
        })
        expected = {'statusCode': 418, 'body': '"I\'m a teapot"'}
        result = rsp['statusCode'] == 418 and rsp['body'] == '"I\'m a teapot"'
        self.record(result, expected, rsp)
    

        # post ping test
        self.header("POST ping test")
        rsp = self.post_request({
            "path":"/ping"
        }, {})
        expected = {'statusCode': 200, 'body': '"pong"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"pong"'
        self.record(result, expected, rsp)

        # route parameters test
        self.header("route parameters test")
        rsp = self.get_request({
            "path":"/hello/john"
        })
        expected = {'statusCode': 200, 'body': '"hello, john"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"hello, john"'
        self.record(result, expected, rsp)

        return self.successful