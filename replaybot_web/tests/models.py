import json
from support.lamb.Test import Test
from models.user import user

class models(Test):
    name = "models"
    
    def run(self):
        test_username = "test-user"
        test_user = user(test_username, "test-user-password")
        test_user_id = test_user.id

        # make sure fillable works
        self.header("model fillable test")
        # hax
        test_user.fillable.append('test_field')
        test_user.update({"test_field": "asdf", "invalid_field": "asdf"})
        fillable = test_user.test_field == "asdf"
        unfillable = test_user.invalid_field != "asdf"
        self.record(fillable and unfillable, "fillable and unfillable", "fillable: " + str(fillable) + ", unfillable: " + str(unfillable))
        
        # return False if no model exists
        self.header("non exist model test")
        tmp = user.get('this-id-probably-doesnt-exist-2342jdfjsdfmnweor')
        self.record(tmp == False, "False", str(tmp))

        # our test model doesnt exist in the db, so we shouldnt be able to get it yet
        self.header("user not saved yet get test")
        tmp = user.get(test_user_id)
        self.record(tmp == False, "False", str(tmp))
        
        # save test
        self.header("save test")
        skip_message = ""
        try:
            # check that we can save our model
            test_user.save()
            # should be in the db now
            tmp = user.get(test_user_id)
            result = tmp.id == test_user_id
        except:
            result = false
            skip_message = "Save test failed"

        self.record(result, "test_user_id", str(tmp))
     
        # find test 
        # if save test failed, skip 
        self.header("model find test")
        if skip_message == "":
            tmp = user.find({ 'username': test_username })
            result = len(tmp) > 0 and tmp[0].username == test_username
            self.record(result, "len(results) > 0 and results[0].username == test_username", str(tmp))
        else:
            skip_message = "Save test failed, nothing to find"
            self.skip(skip_message)

        # delete test 
        # if save test failed, skip 
        self.header("model delete test")
        if skip_message == "":
            result = True
            try:
                test_user.delete()
                # make sure its gone
                tmp = user.get(test_user_id)
                result = tmp == False
            except Exception as e:
                print(e)
                result = False
            self.record(result, "True", str(result))
        else:
            skip_message = "Save test failed, nothing to delete"
            self.skip(skip_message)

        return self.successful