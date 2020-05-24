from framework.lamb.controller import controller
from framework.lamb.http.response import response

class testcontroller(controller):
    def ping(self, event):
        return response(200, "pong")
    def pong(self, event):
        return response(200, event)
    def hello(self, event, name):
        return response(200, "hello, " + name)