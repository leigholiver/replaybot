import json
from framework.lamb.test import test
from support.auth import auth as auth_util
from models.user import user

class auth(test):
    name = "auth"
    
    def run(self):
        au = auth_util()
        test_user = user('asdf-1234')

        self.header("generate token test")
        token = au.token(test_user.id)
        result = au.userid_from_token(token) == test_user.id
        self.record(result, "True", result)

        self.header("verify token test")
        result = au.verify_token(token, test_user.id)
        self.record(result, "True", result)

        self.header("user from token test")
        test_user.save()
        test_user_2 = au.user_from_token(token)
        test_user.delete()
        result = test_user.id == test_user_2.id
        self.record(result, "test_user.id == test_user_2.id", result)

        self.header("expired token test")
        au.ttl = 0
        result = au.verify_token(token, test_user.id)
        self.record(result == False, "False", result)

        self.header("invalid token test")
        result = au.verify_token("invalid-token-wouldnt-that-be-funny-though", test_user.id)
        self.record(result == False, "False", result)


        return self.successful