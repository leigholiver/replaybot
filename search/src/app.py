import sys, os, json
from flask import Flask, Response, request
from elasticsearch import Elasticsearch

index_name       = "replay"
min_query_length = 2
app              = Flask(__name__)
es               = Elasticsearch([os.getenv('ELASTICSEARCH_ENDPOINT')])

@app.route('/ping', methods=["GET"])
def ping():
    return "pong"

@app.route('/list', methods=["GET"])
def list():
    return do_elastic_query(request)

@app.route('/search', methods=["GET"])
def search():
    query = request.args.get('query')
    if not query or len(query) < min_query_length:
        return Response(status=400)
    return do_elastic_query(request, query)

@app.route('/index', methods=["POST"])
def index():
    token = request.headers.get('x-replaybot-token')
    if token != os.getenv('ELASTICSEARCH_PASSWORD'):
        return Response(status=403)

    try:
        doc = request.get_json(force=True)
        es.index(index=index_name, id=doc['id'], body=doc)
        return Response(response='"OK"',
                        status=200,
                        mimetype="application/json")
    except Exception as e:
        print(str(e))
        return Response(status=500)
    return Response(status=400)

def do_elastic_query(request, query = None):
    # params
    limit         = request.args.get('limit') if request.args.get('limit') != None else 10
    cursor        = request.args.get('cursor') if request.args.get('cursor') != None else 0

    # auth
    token = request.headers.get('x-replaybot-token')
    if token != os.getenv('ELASTICSEARCH_PASSWORD'):
        return Response(status=403)
    
    user_channels = request.args.getlist('channels')    
    if not user_channels:
        user_channels = []
    
    search_filter = [{"terms": { "channel": user_channels}}]
    guild_filter = request.args.getlist('guild')
    if guild_filter:
        search_filter.append({"terms": { "guild": guild_filter }})
    
    # set up the query
    search_template = {
        "from":  cursor,
        "size":  limit,
        "query": {"bool": {"filter" : search_filter}}
    }

    if query == None:
        # sort by posted date instead of search relevance
        search_template['sort'] = {"created": "desc"}
    else:
        # set the search term if applicable
        search_template['query']['bool'] = {
            "filter" : search_filter,
            "minimum_should_match" : 1,
            "should": [
                { "match": {"keywords": { "query": query, "fuzziness": "0" }}},
                { "match": {"fuzzykeywords": {"query": query, "fuzziness": "AUTO"}}},
                { "wildcard": {"keywords": {"value": ("%s" % query)}}},
                { "wildcard": {"fuzzykeywords": {"value": ("*%s*" % query)}}}
            ]
        }

    try:
        res = es.search(index=index_name, body=search_template)
        new_cursor = int(cursor) + int(limit)
        if new_cursor < res['hits']['total']['value']:
            res['cursor'] = new_cursor
        return Response(response=json.dumps(res),
            status=200,
            mimetype="application/json")
    except Exception as e:
        print(str(e))
    return Response(status=500)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')