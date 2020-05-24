import os, pkgutil, inspect, json, re
from framework.lamb.model import model
from git import Repo

class env_util():
    environments_dir = "environment/deployments/"
    defaults_path    = "environment/env.json"
    output_file      = "env.auto.tfvars.json"
    
    # fields which can be in environment.json
    # but dont want to be in env.auto.tfvars.json
    # basically to stop terraform complaining about them
    exclude_fields = [
        "branch_specifier", # for matching git branch to environment
        "tf_workspace",     # for overriding the terraform workspace name
        "filename",         # the filename of the env
        "deploy_tests",     # array of tests to run when deploying. default all tests
        "pre_deploy_tasks", # array of lambctl arguments to run before deploying
        "post_deploy_tasks" # array of lambctl arguments to run after deploying
    ]

    def setup_env(self, args):
        defaults = self.get_defaults()
        os.environ["PROJECT_NAME"] = defaults['project_name']

        env_name = "local"
        if "--live" in args:
            args.remove("--live")
            env_name = self.get_name(True)
            if not env_name:
                return False
        os.environ["LAMB_ENV"] = env_name
        
        return True

    def get_name(self, ignore_env=False):
        if os.getenv('LAMB_ENV') != None and not ignore_env:
            return os.getenv('LAMB_ENV')
        
        e = self.get_full()
        if e != False:
            return e['env_name']
        return False

    def get_full(self):
        envs = self.get_environments()
        if envs == []:
            print("No environment definitions found")
            return False

        data = self.get_from_env_var(envs)
        if data != False:
            return data

        data = self.get_from_git(envs)
        if data != False:
            return data

        if os.getenv('LAMB_ENV') == "local":
            return self.get_defaults()

        return False

    def get_tf_vars(self):
        e = self.get_full()
        if e == False:
            return False
            
        self.process_cron(e)
        self.process_buckets(e)
        self.process_secrets(e)

        # process models/tables
        tables = self.scan_for_tables(["models", "framework.tests.support.models"])
        e['tables'] = tables
        
        # clean up
        for field in self.exclude_fields:
            e.pop(field, None)
        return e

    def export_tf_vars(self):
        e = self.get_tf_vars()
        env_output = json.dumps(e, indent=4, sort_keys=True)
        try:
            with open(self.output_file, "w") as file:
                file.write(env_output)
        except:
            print("error writing environment file")
            return False
        return True

    def verify_environments(self):
        envs = self.get_environments()
        
        errors = []
        for e in envs:
            # check against other environments
            for f in envs:
                if 'filename' in e.keys() and 'filename' in f.keys() and e['filename'] != f['filename']:
                    if 'domain_name' in e.keys() and 'domain_name' in f.keys() and e['domain_name'] == f['domain_name']:
                        self.add_error(errors, "warning: duplicate domain " + e['domain_name'] + " - " + e['filename'] + " and " + f['filename'])

                    if e['env_name'] == f['env_name']:
                        self.add_error(errors, "warning: duplicate name " + e['env_name'] + " - " + e['filename'] + " and " + f['filename'])

                    if "tf_workspace" in e.keys() and e['tf_workspace'] == f['env_name']:
                        self.add_error(errors, "warning: terraform workspace " + e['tf_workspace'] + " in " + e['filename'] + " conflicts with name " + f['env_name'] + " in " + f['filename'])

                    if "tf_workspace" in e.keys() and "tf_workspace" in f.keys() and e['tf_workspace'] == f['tf_workspace']:
                        self.add_error(errors, "warning: terraform workspace " + e['tf_workspace'] + " in " + e['filename'] + " conflicts with workspace " + f['tf_workspace'] + " in " + f['filename'])

            # check buckets
            if "buckets" in e.keys():
                seen_root = False
                for b in e["buckets"]:
                    if 'subdomain' not in b.keys():
                        if seen_root:
                            self.add_error(errors, "warning: found multiple root s3 buckets in " + e['filename'])
                        seen_root = True

                    seen_self = False
                    for c in e["buckets"]:
                        if b != c:
                            if b['content_dir'] == c['content_dir']:
                                self.add_error(errors, "warning: duplicate content dir " + b['content_dir'] + " in " + e['filename'])
                            if 'subdomain' in b.keys() and 'subdomain' in c.keys() and b['subdomain'] == c['subdomain']:
                                self.add_error(errors, "warning: duplicate bucket subdomain " + b['subdomain'] + " in " + e['filename'])
                        else:
                            if seen_self:
                                self.add_error(errors, "warning: duplicate bucket definition " + b['content_dir'] + " in " + e['filename'])
                            seen_self = True

        for error in errors:
            print(error)
        return len(errors) == 0

    def add_error(self, errors, error):
        if error not in errors:
            errors.append(error)

    def process_cron(self, e):
        if 'cron_jobs' in e.keys():
            for job in e['cron_jobs']:
                job['data'] = json.dumps(job['data'])

    def process_buckets(self, e):
        if 'buckets' in e.keys():
            for bucket in e['buckets']:
                keys = [ "subdomain", "use_react_router" ]
                for k in keys:
                    if k not in bucket.keys():
                        bucket[k] = ""
                    elif k == 'subdomain' and bucket[k] != "":
                        if 'dns_names' not in e.keys():
                            e['dns_names'] = []
                        e['dns_names'].append({
                            'name': bucket[k] + "." + e['domain_name'],
                            'value': "s3-website.eu-west-2.amazonaws.com",
                            'type': "CNAME"
                        })

    def process_secrets(self, e):
        if 'env_vars' in e.keys():
            for key in e['env_vars'].keys():
                match = re.search("{{ secrets\.(.*) }}", e['env_vars'][key])
                if match:
                    e['env_vars'][key] = e['env_vars'][key].replace(match.group(0), str(os.getenv(match.group(1))))
        
        if 'allowed_ips' in e.keys():
            for i in range(0, len(e['allowed_ips'])):
                match = re.search("{{ secrets\.(.*) }}", e['allowed_ips'][i])
                if match:
                    e['allowed_ips'][i] = e['allowed_ips'][i].replace(match.group(0), str(os.getenv(match.group(1))))

    def get_from_env_var(self, envs):
        for e in envs:
            if os.getenv('LAMB_ENV') == e['env_name']:
                return e
        return False

    def get_from_git(self, envs):
        try:
            repo = Repo(os.getcwd())
        except:
            # hack for replaybot because the git repo is in the folder above
            # todo: implement a base_git_path variable 
            repo = Repo(os.path.abspath("../"))
        
        try:
            branch = repo.active_branch.name
        except Exception as e:
            print(e)
            return False

        for e in envs:
            match = re.search(e['branch_specifier'], branch)
            if (match):
                return e
        return False

    # this is dumb but we kind of need to combine the arrays so w/e
    def combine_with_defaults(self, data):
        defaults = self.get_defaults()
        out = defaults.copy()
        for key in data.keys():
            # merge lists
            if key in out.keys() and isinstance(out[key], list):
                out[key] = out[key] + data[key]
            # merge dicts
            elif key in out.keys() and isinstance(out[key], dict):
                out[key].update(data[key])
            else:
                out[key] = data[key]
        return out

    def get_defaults(self):
        return json.load(open(self.defaults_path))

    def get_environments(self):
        files = os.listdir(self.environments_dir)
        envs = []
        defaults = self.get_defaults()
        for file in files:
            if file.endswith(".json"):
                try:
                    with open(self.environments_dir + file) as json_file:
                        data = json.load(json_file)
                        if "env_name" in data.keys() and \
                                "branch_specifier" in data.keys():
                            data['filename'] = file
                            envs.append(self.combine_with_defaults(data))
                        else:
                            print("skipping " + file + " - missing env_name or branch_specifier")
                except Exception as e:
                    print(e)
                    print("skipping " + file + " - error parsing json")

        return envs

    def scan_for_tables(self, packages = ["models"]):
        table_names = []
        for package in packages:
            try:
                imported_package = __import__(package, fromlist=['blah'])
                for _, pluginname, ispkg in pkgutil.iter_modules(imported_package.__path__, imported_package.__name__ + '.'):
                    if not ispkg:
                        try:
                            plugin_module = __import__(pluginname, fromlist=['blah'])
                            clsmembers = inspect.getmembers(plugin_module, inspect.isclass)
                            for (_, c) in clsmembers:
                                if issubclass(c, model) & (c is not model):
                                    m = c()
                                    table_names.append({ "name": m.table, "indexes": m.indexes, "sort_key": m.sort_key, "expires": m.expires})
                        except Exception as e:
                            print("error scanning for tables: " + str(e))
            except:
                print("warning: couldn't scan for models in " + package)
        return table_names