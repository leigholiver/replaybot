import os
from framework.lamb.middleware import middleware

class hasbottoken(middleware):
    def process(self, event):
        if self.is_bot(event):
            return event
        self.reject()

    def is_bot(self, event):
        token = self.header("X-Replaybot-Token", event)
        if not token:
            token = self.header("x-replaybot-token", event)
        if token == os.getenv('BOT_SHARED_KEY'):
            return True
        return False