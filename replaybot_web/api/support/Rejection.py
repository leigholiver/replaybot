class Rejection(Exception):
    def __init__(self, statusCode, body):
        self.statusCode = statusCode
        self.body = body