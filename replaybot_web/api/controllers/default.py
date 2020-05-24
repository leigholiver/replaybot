from framework.lamb.controller import controller

class default(controller):
    def ping(self, event):
        # process the event here and return a response
        
        return self.respond(200, "pong")