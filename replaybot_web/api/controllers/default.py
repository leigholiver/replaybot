from support.lamb.Controller import Controller

class default(Controller):
    def ping(self, event):
        # process the event here and return a response
        
        return self.respond(200, "pong")