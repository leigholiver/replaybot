## replaybot_search

bridge to elasticsearch

#### `GET /ping`
returns pong if everything is ok


#### `POST /index`

index a replay. post body should be the json object to index. see `replaybot_web/api/support/indexer.py get_document()`


#### `GET /list`

get a paginated list of replays

`@param cursor` [optional] elasticsearch pagination cursor

`@param limit` [optional, default 15] number of results to return


#### `GET /search`

search the replays

`@param query` search terms

`@param cursor` [optional] elasticsearch pagination cursor

`@param limit` [optional, default 15] number of results to return



`sudo docker build -t replaybot_search .`

`sudo docker run --rm -p5002:5002 --name replaybot_search replaybot_search`
