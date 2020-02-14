import sys, os, pkgutil, inspect
from support.lamb.Command import Command
from support.lamb.Test import Test

class tests(Command):
    def run(self, data):

        tests = []
        if len(data) > 0:
            for t in data:
                tmp = self.testsFromClassName("tests." + t)
                if tmp == []:
                    print("Test " + t + " not found.")
                tests += tmp

            if tests == []:
                print("No tests to run.")
                return False
        else:
            tests = self.scanForTests()

        all_test = Test()
        if len(tests) > 1:
            all_test.header("Running Tests...")
        
        for test in tests:
            all_test.header(" --- Running test: " + test.name + " --- ")
            t = test()
            
            try:
                result = t.run()
            except Exception as e:
                all_test.warn(" --- Exception in test: " + test.name + " --- ")
                all_test.fail(str(e.__class__) + ": " + str(e))
                result = False

            if result:
                all_test.success(" --- " + test.name + " --- ")
            else:
                all_test.fail(" --- " + test.name + " --- ")
        
        if len(tests) > 1:
            if all_test.successful:
                all_test.success("Tests Succeeded!")
            else:
                all_test.fail("Tests Failed")

        return all_test.successful

    def scanForTests(self):
        test_names = []
        imported_package = __import__("tests", fromlist=['blah'])
        for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
            if not ispkg:
                try:
                    test_names += self.testsFromClassName(pluginname)
                except Exception as e:
                    print(e)
                    pass
        return test_names

    def testsFromClassName(self, classname):
        test_names = []
        try:
            plugin_module = __import__(classname, fromlist=['blah'])
            clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, c) in clsmembers:
                if issubclass(c, Test) & (c is not Test):
                    test_names.append(c)
        except Exception as e:
            print(e)
            pass

        return test_names