### lamb

![Tests](https://github.com/leigholiver/lamb/workflows/Tests/badge.svg) ![Deployment](https://github.com/leigholiver/lamb/workflows/Deployment/badge.svg)

python framework using aws api gateway/lambda/dynamodb/s3/cloudflare workers. this is a weekend hobby project made for fun, it is probably not wise to use it


#### configuration/setup

configuration is handled through `environment/env.json`. you can override any variable from `environment.tf` in this file. you can specify additional per-environment overrides in a json file in `environment/deployments/`

`lambctl` commands:

`./lambctl env create` create a new environment json in `environment/deployments/`

`./lambctl make [command|controller|middleware|model|test] [name]` create class files

`./lambctl tests [optional test names]` run all/specified tests

`./lambctl deploy [-y|-auto-approve|--skip-tests|--ignore-tests]` deploy the application

`./lambctl make command [name]` create custom lambctl commands

you can run your command using `./lambctl [name]`, which will call `run(self, data)` where `data` is an array of the arguments passed to lambctl. by default `lambctl` will use the built in tinydb database, add `--live` to use the environment dynamodb backend instead.

you can specify commands to run before/after deployment by setting the `pre_deploy_tasks` and `post_deploy_tasks` field of your `environment.json`

```
"pre_deploy_tasks": [
    ["build_frontend", "--some-flag"]
],
"post_deploy_tasks": [
    ["tests", "--live"],
    ["seed", "--live"]
]
```

you can schedule commands by adding to the `cron_jobs` field of your `environment.json`. cron jobs will use the environment dynamodb backend.

```
"cron_jobs": [{
    "name": "cron_test",            # the name of the scheduled job
    "rate": "rate(10 minutes)",     # can be any string understood by cloudwatch, cron(0 20 * * ? *) or rate(5 minutes)
    "data": [                       # list of arguments to pass to lambctl
        "testcommand",
        "--some-argument"
    ]
}]
```

adding s3 bucket websites to `environment.json`:

```
"buckets": [{
    "content_dir": "./public", # local directory containing the content
    "subdomain": "public",     # [optional once] subdomain to use (https://public.yourdomain.com), if left blank will use your domain name
    "use_react_router": "true" # [optional] if set to true, will add routing rules to add react-router compatibility (404 responses will redirect to /#!/)
}]
```

you can specify secrets from `secrets.env` in your `environment.json` in the `allowed_ips` and `env_vars` fields

```
"allowed_ips": [ "{{ secrets.ALLOWED_IP }}" ],
"env_vars": {
    "JWT_SECRET": "{{ secrets.JWT_SECRET }}"
}
```

#### controllers

`./lambctl make controller [name]`

a controller contains one or many route functions, which accept an `event` parameter and returns a response using `self.respond(status_code, response_body)`. the `event` parameter is a dict as passed through from api gateway, so you can use the usual ways of getting query params, headers and post body

you can pass additional parameters from the url path from the route definition using the parameter name within brackets - `example(self, event, id, slug)` would use the path `/(id)/(slug)` 

routes are defined in `api/routes.py`

```
routes = [
    "/test/(id)": {                   # the path for the route
        "methods": [ "GET", "POST" ], # one or more of any method supported by lambda/api gateway
        "action": "default.ping",     # controller function, in the format class.function
        "middleware": [               # array of middleware to run before the request hits the controller
            "test"
        ]
    },
]
```


#### middleware

`./lambctl make middleware [name]`

implement `process(self, event)` and return the processed "event"

you can call `self.reject()` to block the request and return a 403 response, or with a custom http status: `self.reject(statusCode, body)`


#### models

`./lambctl make model [name]`

`self.table` is the name to use for the table

`self.fillable` is an array of fields which are allowed to be updated from the api/update() function

`self.indexes` is an array of fields to use as indexes

`model.find({"index": "query" })` will query the table for models matching a specified index

`model.get(id)` will return the object of that id from the `model` table

`model.save()` will store the object to the db

`model.delete()` will delete the object from the db

todo: searching/indexing type stuff


#### tests

`./lambctl make test [name]`

`./lambctl tests [optional names of tests to run]`

your test should `return self.successful`. use `self.record(name, result, expected, response)` to track stages of your test. 

helper functions to record output to the terminal with colours where supported: `self.header(message)`, `self.info(message="")`,`self.skip(message="")`, `self.warn(message)`, `self.fail(message="")`. using `self.fail()` will mark your test failed as well as printing the message

You can query the api locally using `self.get_request(request)` or `self.post_request(request, post_data)` where `request` is a dict of any event field you wish to override (path, query string parameters, method, headers etc. `{"path":"/ping"}` for example) and `post_data` is a dict to use as the request body


#### development server

`./lambctl dev` will start the local development server, which uses flask and tinydb

`http://localhost:5000/` the root bucket

`http://localhost:5000/api` the api endpoint

`http://localhost:5000/[bucket subdomain]` additional buckets

todo: customise dev server ports

todo: i'd like to get this all working with localstack for consistency but it doesn't like the permissions weirdness in the terraform. i'll come back to it probably. this development server will hot reload routes/code/bucket contents etc so it might be more suited for development, but it would be nice to have a local integration env

todo: dockerise the dev/lambctl environment? maybe something like, start the dev server in a screen, drop to a shell for lambctl? some volume mount for existing projects/script to create a new project if its empty?


#### deployment

terraform should use your aws cli configuration, you can set the `aws_profile` variable in your environment json to switch profiles

`cp secrets.env.example secrets.env` and fill in the required info

update `environment/deployments/master.json` with your domain name

update `environment/state.tfvars` with the information of an s3 bucket to store state in

deployment is handled through github actions scripts which:
- run tests on pull requests
- deploy on push to staging/master branches

you need to set a secret in your github repo called `secrets` containing a `secrets.env`

`./lambctl deploy [-auto-approve|-y] [--ignore-tests|--skip-tests]` to deploy manually 

specify tests to run before deployment using the `deploy_tests` variable in the environment json. `--ignore-tests` will deploy even if tests fail, `--skip-tests` will skip the tests entirely


#### manual deployment steps

- `./lambctl env verify export` verify your environment definitions and generate the `env.auto.tfvars.json` file for the current environment

- `./lambctl routes` generate the compiled routes file

- `./lambctl gather` package the api lambda (manual sub steps below: )

    - `cp -r api/* .build` copy the api files into the build dir

    - `mkdir -p ./build/framework && cp -r framework/lamb .build/framework` add the framework support files

    - `pip install -r api/packages.txt -t ./build` package the dependencies

- run any pre deploy tasks

- `./lambctl tests` run your tests

- `terraform init -backend-config=environment/state.tfvars`

- `terraform workspace select [environment] || terraform workspace new [environment]` set up the terraform workspace

- `terraform [plan/apply/destroy]` control the deployment

- run any post deploy tests