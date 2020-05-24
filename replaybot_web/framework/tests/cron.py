import json
from framework.lamb.test import test
from framework.lamb.http.lambda_handler import lambda_handler

class cron(test):
    name = "cron"
    def run(self):
        self.header("Cron test - Run Test command via Cron")
        result = self.run_cron(["test_command"])
        self.record(result, "Success", "Success" if result else "Failure")

        self.header("Wool test")
        result = self.run_cron(["wool"])
        self.record(result, "Success", "Success" if result else "Failure")
        
        return self.successful

    def run_cron(self, data):
        data_str = json.dumps(data)
        result = True    
        try:
            self.info(" -- CRON OUTPUT -- ")
            output = lambda_handler(data_str, {})
            self.info(" -- END CRON OUTPUT -- ")
            
            result = output['statusCode'] == 200
        except Exception as e:
            print(e)
            result = False

        return result