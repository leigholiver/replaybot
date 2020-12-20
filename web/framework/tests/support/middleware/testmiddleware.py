from framework.lamb.middleware import middleware

class testmiddleware(middleware):
    def process(self, event):
        # arbitrarily reject with a 403
        if isinstance(event['queryStringParameters'], dict) and 'reject' in event['queryStringParameters'].keys():
            self.reject()

        # reject with a specific status code and message
        if isinstance(event['queryStringParameters'], dict) and 'teapot' in event['queryStringParameters'].keys():
            self.reject(418, "I'm a teapot")

        # inject fields into the event
        event['MiddlewareInjected'] = "This request was passed through ExampleMiddleware"
        
        return event