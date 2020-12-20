## replaybot_discord

the "bot" in replaybot

required environment variables:

`DISCORD_TOKEN` - discord api token

`PARSER_ENDPOINT` - url to post replay urls to for parsing

`API_ENDPOINT` - url for the replaybot api - for server tracking and replay posting goodness

`API_TOKEN` - pre shared key, must match the key set on the api or events will be rejected



`sudo docker build -t replaybot_discord .`

```
sudo docker run --rm \
-e DISCORD_TOKEN=[ your discord token ] \
-e PARSER_ENDPOINT=$PARSER_ENDPOINT \
-e API_ENDPOINT=$API_ENDPOINT \
-e API_TOKEN=$API_TOKEN \
--name replaybot_discord replaybot_discord


# if you want to run the mock server that blindly 200s
python mock_server.py

# change this to whatever your parser endpoint is
# you need the docker host ip instead of localhost
export PARSER_ENDPOINT=http://$(ip -4 addr show docker0 | grep -Po 'inet \K[\d.]+'):8119
```