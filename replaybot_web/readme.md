## replaybot_web

web interface for replaybot


### deployment

`cp .env.example .env`, add the required values, `source .env`

`./lambctl deploy` deploy or update

`-auto-approve` or `-y` will pass the -auto-approve flag to terraform

`--ignore-tests` ignore results of tests and deploy anyway

`--skip-tests` skips tests entirely

made using [lamb](https://github.com/leigholiver/lamb)