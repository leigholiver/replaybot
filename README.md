## Replaybot

a discord bot to post information about sc2 replays

[replaybot.com](https://www.replaybot.com)

![Tests](https://github.com/leigholiver/replaybot/workflows/Tests/badge.svg) ![Deployment](https://github.com/leigholiver/replaybot/workflows/Deployment/badge.svg)
![Build-Parser](https://github.com/leigholiver/replaybot/workflows/Build-Parser/badge.svg) ![Build-Discord](https://github.com/leigholiver/replaybot/workflows/Build-Discord/badge.svg)

#### Development server

`. replaybot_web/secrets.env && sudo -E docker-compose up` to run the parser + discord bot

`cd replaybot_web && ./lambctl dev` to run the web services

to run the bot against a different api just modify the `API_ENDPOINT` environment var in `docker-compose.yml`


#### Database utils

`util/migrate.sh [source table] [destination table]` migrate the data from one dynamodb table into another, for example for transferring between environments

`util/devdb.sh [source table] [model name]` download the data from dynamodb and put it into the relevant local tinydb file

`util/export.sh [source table] [filename]` export the data from a dynamodb table to a json file