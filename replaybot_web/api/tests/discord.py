import os
from framework.lamb.test import test

class discord(test):
    name = "discord"
    
    def run(self):
        self.header("discord code test")
        if not os.getenv('CI'):
            print("please go to this url in your browser, and once authorized and redirected, enter the code= parameter from the url")
            print("https://discord.com/api/oauth2/authorize?client_id=" + os.getenv('CLIENT_ID') + "&redirect_uri=http%3A%2F%2Flocalhost%3A3000%2Fdiscord&response_type=code&scope=identify%20guilds")
            code = input("code=")
            rsp = self.post_request({
                "path":"/discord-code",
                "queryStringParameters": {
                    "code": code
                }
            }, {})
            expected = { 'statusCode': 200 }
            result = rsp['statusCode'] == 200
            self.record(result, expected, rsp)
        else:
            self.skip("cannot run discord test in CI, skipping")

        return self.successful