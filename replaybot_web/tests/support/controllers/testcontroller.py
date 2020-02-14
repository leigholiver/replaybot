from support.lamb.Controller import Controller

class testcontroller(Controller):
    def ping(self, event):
        return self.respond(200, "pong")
    def pong(self, event):
        return self.respond(200, event)
    def hello(self, event, name):
        return self.respond(200, "hello, " + name)