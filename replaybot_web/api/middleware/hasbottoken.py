import os
from support.lamb.Middleware import Middleware

class hasbottoken(Middleware):
    def process(self, event):
        if self.is_bot(event):
            return event
        self.reject()

    def is_bot(self, event):
        if isinstance(event['headers'], dict) and "X-Replaybot-Token" in event['headers'].keys():
            if event['headers']["X-Replaybot-Token"] == os.getenv('BOT_SHARED_KEY'):
                return True
        return False