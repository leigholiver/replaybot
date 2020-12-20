# Replaybot

a discord bot to post information about sc2 replays

[replaybot.com](https://www.replaybot.com)

![Tests](https://github.com/leigholiver/replaybot/workflows/Tests/badge.svg) ![Deployment](https://github.com/leigholiver/replaybot/workflows/Deployment/badge.svg)
![Build-Parser](https://github.com/leigholiver/replaybot/workflows/Build-Parser/badge.svg) ![Build-Discord](https://github.com/leigholiver/replaybot/workflows/Build-Discord/badge.svg)


## Development server
```bash
# install the dependencies
pip install -r web/framework/requirements.txt
pip install -r web/api/packages.txt

# start the development server
make dev
```

if you get a bunch of `Expecting property name enclosed in double quotes: line 1 column 206 (char 205)` errors - stop the dev server, delete `web/.localdb/replaybot_local_job_queue.json`, and restart the dev server


#### starting dev server parts individually:

`cd web && ./lambctl dev` to run the api dev server, react dev server, and dev queue worker (`make lamb`)

`. web/secrets.env && sudo -E docker-compose up` to run the parser/discord bot/search api/elasticsearch (`make docker`)


## Database utils

`util/migrate.sh [source table] [destination table]` migrate the data from one dynamodb table into another, for example for transferring between environments

`util/devdb.sh [source table] [model name]` download the data from dynamodb and put it into the relevant local tinydb file

`util/export.sh [source table] [filename]` export the data from a dynamodb table to a json file
