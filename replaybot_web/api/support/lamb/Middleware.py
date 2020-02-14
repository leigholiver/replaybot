from support.Rejection import Rejection

class Middleware():
    def process(self, event):
        pass

    def reject(self, statusCode = 403, body = '"Forbidden"'):
        raise Rejection(statusCode, body)