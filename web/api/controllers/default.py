from framework.lamb.controller import controller
from framework.lamb.queue.queue_util import queue_util

class default(controller):
    def ping(self, event):
        # process the event here and return a response
        return self.respond(200, "pong")