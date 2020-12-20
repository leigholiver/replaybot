from framework.lamb.middleware import middleware
from support.auth import auth as auth_util

class auth(middleware):
    def process(self, event):
        au = auth_util()
        token = self.header("Authorization", event)
        if not token:
            token = self.header("authorization", event)
            if not token:
                self.reject()
        user = au.user_from_token(token)
        if not user:
            self.reject()
        event['logged_in_user'] = user
        return event