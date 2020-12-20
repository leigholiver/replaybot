class handlerinterface():
    # return true if the event can be processed by this handler
    def is_valid(self, event):
        return False
    
    # process the event and return a response
    def handle(self, event, context):
        return False