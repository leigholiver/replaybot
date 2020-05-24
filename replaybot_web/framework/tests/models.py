import json, os, datetime
from framework.lamb.test import test
from framework.tests.support.models.test_model import test_model

class models(test):
    name = "models"
    
    def run(self):
        # params
        test_index_value = "test-index-value"
        sort_test_model_count = 10

        # setup
        model = test_model()
        model.test_index = test_index_value
        test_id = model.id

        # make sure fillable works
        self.header("model fillable test")
        # hax
        model.fillable.append('test_field')
        model.update({"test_field": "asdf", "invalid_field": "asdf"})
        fillable = model.test_field == "asdf"
        unfillable = model.invalid_field != "asdf"
        self.record(fillable and unfillable, "fillable and unfillable", "fillable: " + str(fillable) + ", unfillable: " + str(unfillable))
        
        # return False if no model exists
        self.header("non exist model test")
        tmp = test_model.get('this-id-probably-doesnt-exist-2342jdfjsdfmnweor')
        self.record(tmp == False, "False", str(tmp))

        # our test model doesnt exist in the db, so we shouldnt be able to get it yet
        self.header("model not saved yet get test")
        tmp = test_model.get(test_id)
        self.record(tmp == False, "False", str(tmp))
        
        # save test
        self.header("save test")
        skip_message = ""
        try:
            # check that we can save our model
            model.save()
            # should be in the db now
            tmp = test_model.get(test_id)
            result = tmp.id == test_id
        except Exception as e:
            print(e)
            result = False
            skip_message = "Save test failed"

        self.record(result, test_id, str(tmp))
     
        # find test 
        # if save test failed, skip 
        self.header("model find by index test")
        if skip_message == "":
            tmp = test_model.find({ 'test_index': test_index_value })
            result = len(tmp) > 0 and tmp[0].test_index == test_index_value
            self.record(result, "len(results) > 0 and results[0].test_index == test_index_value", str(tmp))
        else:
            skip_message = "Save test failed, nothing to find"
            self.skip(skip_message)

        # delete test, if save test failed, skip 
        self.header("model delete test")
        if skip_message == "":
            result = True
            try:
                model.delete()
                # make sure its gone
                tmp = test_model.get(test_id)
                result = tmp == False
            except Exception as e:
                print(e)
                result = False
            self.record(result, "True", str(result))
            if not result:
                skip_message = "Delete test failed"
        else:
            skip_message = "Save test failed, nothing to delete"
            self.skip(skip_message)

        # sort key test
        self.header("sort key tests")
        if skip_message == "":
            test_models = []
            no_models_time = datetime.datetime.now().isoformat()

            try:
                # set up the models
                self.info("setting up test models...")
                for i in range(0, sort_test_model_count):
                    tmp = test_model()
                    test_models.append(tmp)
                    tmp.save()

                self.header("direction asc")
                # test that the sort key / direction works
                tmp = test_model.list(limit=1)
                result = tmp[0].id == test_models[0].id
                self.record(result, "tmp.id == " + test_models[0].id, "tmp.id == " + tmp[0].id)

                self.header("direction desc")
                tmp = test_model.list(limit=1, direction="desc")
                result = tmp[0].id == test_models[len(test_models)-1].id
                self.record(result, "tmp.id == " + test_models[len(test_models)-1].id, "tmp.id == " + tmp[0].id)

                # test that the limit works
                self.header("single result limit")
                result = len(tmp) == 1
                self.record(result, "len(tmp) == 1", "len(tmp) == " + str(len(tmp)))

                self.header("3 result limit")
                tmp = test_model.list(limit=3)
                result = len(tmp) == 3
                self.record(result, "len(tmp) == 3", "len(tmp) == " + str(len(tmp)))

                # test that the before function works
                self.header("0 results from before we created")
                tmp = test_model.list(before = no_models_time)
                result = len(tmp) == 0
                self.record(result, "len(tmp) == 0", "len(tmp) == " + str(len(tmp)))

                self.header(str(len(test_models)-1) + " results from before model " + str(len(test_models)-1) + " was created")
                tmp = test_model.list(before = test_models[3].created)
                result = len(tmp) == 3
                self.record(result, "len(tmp) == " + str(len(test_models)-1), "len(tmp) == " + str(len(tmp)))

            except Exception as e:
                print(e)
                self.record(False, "", "Error in test, aborting")

            for tmp in test_models:
                tmp.delete()
        else:
            skip_message = "either save or delete test failed, sort test cannot continue"
            self.skip(skip_message)

        return self.successful