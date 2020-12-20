from framework.lamb.http.rejection import rejection

class middleware():
    def process(self, event):
        pass

    def reject(self, statusCode = 403, body = "Forbidden"):
        raise rejection(statusCode, body)

    def header(self, header, event):
        if isinstance(event['headers'], dict) and header in event["headers"].keys():
            return event['headers'][header]
        return False