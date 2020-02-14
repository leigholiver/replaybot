from support.lamb.Test import Test
import uuid
from models.server import server

class bothacks(Test):
    name = "bothacks"
    
    def run(self):


        test_server_id = str(uuid.uuid4())
        test_server = server(test_server_id)
        test_server.save()

        self.header("get server with bot token test")
        rsp = self.getRequest({
            "path": "/servers/" + test_server_id,
            "headers": {"X-Replaybot-Token": "1234"}
        })
        expected = {'statusCode': 200}
        result = rsp['statusCode'] == 200 
        self.record(result, expected, rsp)
       
        test_server.delete()

        return self.successful