from support.lamb.Test import Test

class discord(Test):
    name = "discord"
    
    def run(self):
        self.header("discord code test")
        rsp = self.postRequest({
            "path":"/discord-code",
            "queryStringParameters": {
                "code": "LKzXvQPamkE0STTVE2aPlq33FceGJL"
            }
        }, {})
        expected = {'statusCode': 200, 'body': '"pong"'}
        result = rsp['statusCode'] == 200 and rsp['body'] == '"pong"'
        self.record(result, expected, rsp)

        return self.successful


        