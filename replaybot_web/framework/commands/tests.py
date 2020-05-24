import sys, os, pkgutil, inspect
from framework.lamb.command import command
from framework.lamb.test import test

class tests(command):
    def run(self, data):

        tests    = []
        failures = []
        all_test = test()

        if len(data) > 0:
            for t in data:
                tmp = self.tests_from_classname("tests." + t)
                if tmp == False:
                    all_test.fail("error creating test " + t)
                elif tmp == []:
                    all_test.fail("test " + t + " not found.")
                else:
                    tests += tmp
            if tests == []:
                all_test.fail("No tests to run")
        else:
            tests = self.scan_for_tests(lambda name: all_test.fail("Error loading test " + name))

        if len(tests) > 1:
            all_test.header("Running Tests...")
        
        for t in tests:
            all_test.header(" --- Running test: " + t.name + " --- ")
            try:
                test_obj = t()
                result = test_obj.run()
            except Exception as e:
                all_test.warn(" --- Exception in test: " + t.name + " --- ")
                all_test.fail(str(e.__class__) + ": " + str(e))
                failures.append(t.name + ": Exception: " + str(e.__class__) + ": " + str(e))
                result = False

            if result:
                all_test.success(" --- " + t.name + " --- ")
            else:
                all_test.fail(" --- " + t.name + " --- ")
                failures.append(t.name + ": Test Failed")
        
        if len(tests) > 1:
            if all_test.successful:
                all_test.success("Tests Succeeded!")
            else:
                all_test.fail("Tests Failed")
                all_test.info("--- Failures ---")
                for failure in failures:
                    all_test.info(failure)

        return all_test.successful

    # callback is function to call if a test load fails
    def scan_for_tests(self, callback = None):
        test_names = []
        packages = [ "tests", "framework.tests" ]
        imported_packages = []
        
        for package in packages:
            try:
                tmp = __import__(package, fromlist=[""])
                imported_packages.append(tmp)
            except:
                print("warning: couldn't import package " + package)
                
        for imported_package in imported_packages:
            for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
                if not ispkg:
                    tmp_test = self.tests_from_classname(pluginname)
                    if not tmp_test:
                        if callback != None:
                            callback(pluginname)
                    else:
                        test_names += tmp_test
        return test_names

    def tests_from_classname(self, classname):
        test_names = []
        try:
            plugin_module = __import__(classname, fromlist=[""])
        except ModuleNotFoundError as e:
            print(e)
            try:
                plugin_module = __import__("framework." + classname, fromlist=[""])
            except ModuleNotFoundError as e:
                print(e)
                return False

        try:
            clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
            for (_, c) in clsmembers:
                if issubclass(c, test) & (c is not test):
                    test_names.append(c)
        except Exception as e:
            print(e)
            return False
            
        return test_names