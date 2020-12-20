import os, json, sys, requests, datetime
from itertools import permutations
from models.replay import replay

class indexer():
    def index_from_data(self, replay_data):
        rep = replay()
        rep.data = replay_data
        return self.index(rep) == "OK"

    def index(self, replay):
        return self.do_api_request("POST", "/index", json=self.get_document(replay))

    def list(self, channels, guild=None, cursor = None):
        return self.do_api_request("GET", "/list", params={'cursor': cursor}, guild=guild, channels=channels)

    def search(self, channels, query, guild = None, cursor = None):
        return self.do_api_request("GET", "/search", params={'query': query, 'cursor': cursor}, guild=guild, channels=channels)

    def do_api_request(self, method, endpoint, params = None, json = None, guild=None, channels=[]):
        params = params if params != None else []
        if type(params) == dict:
            params = [(k, v) for k, v in params.items()]

        for chan in channels:
            params.append(('channels', chan))
        
        if guild:
            params.append(('guild', guild))

        try:
            r = requests.request(method, os.getenv('SEARCH_ENDPOINT') + endpoint, 
                headers={'x-replaybot-token': os.getenv('ELASTICSEARCH_PASSWORD')},
                params=params, json=json
            )
            if r.status_code != 200:
                print("got response code " + str(r.status_code) + " from search")
                return False
            return r.json()
        except Exception as e:
            raise e
            return False

    # parse the replay into the document format
    def get_document(self, replay):
        words         = self.get_keywords(replay)
        keywords      = ", ".join(words['keywords'])
        fuzzykeywords = ", ".join(words['fuzzykeywords'])
        
        # wild hacks for indexing replays from pre-search times
        # todo: once all the replays have been indexed this can be 
        # removed, it will be fixed as part of the indexing process
        if replay.created == None:
            # there is a real mess of stuff in the database :/
            date_check = replay.replay_data['replayData']['timeUTC'] / 1000
            if date_check > 1262304000:
                replay.replay_data['replayData']['timeUTC'] = date_check
                for player in replay.replay_data['replayData']['players']:
                    player['team_id'] = player['team_id'] + 1
            replay.created = datetime.datetime.fromtimestamp(replay.replay_data['replayData']['timeUTC']).isoformat()
        # end hack

        rep = {
            'id':            replay.id,
            'guild':         replay.replay_data['source']['guild']['id'],
            'channel':       replay.replay_data['source']['channel']['id'],
            'created':       replay.created,
            'keywords':      keywords,
            'fuzzykeywords': fuzzykeywords,
            'replay':        replay.replay_data
        }
        return rep
        
    # brute force generate some useful keywords
    def get_keywords(self, replay):
        keywords = {
            "keywords": [],
            "fuzzykeywords": [
                replay.replay_data['replayData']['map'],
                replay.replay_data['source']['author']['name'],
                replay.replay_data['source']['channel']['name'],
                replay.replay_data['source']['guild']['name'],
                replay.replay_data['url']
            ]
        }
        
        if replay.replay_data['message'] != "\n":
            keywords['fuzzykeywords'].append(json.dumps(replay.replay_data['message']))

        teams = {}
        
        # fields from the player object to pull as-is
        player_keywords = ['race', 'name', 'clan', 'profile_url']
        for player in replay.replay_data['replayData']['players']:
            for k in player_keywords:
                if not player[k] in keywords['fuzzykeywords'] and type(player[k]) == str:
                    keywords['fuzzykeywords'].append(player[k])

            # (5123) => [ '5k', '5.1k']
            if 'mmr' in player.keys():
                mmr = str(player['mmr'])
                if(len(mmr) == 4):
                    mmr_strings = [ str(player['mmr'])[0] + "k", str(player['mmr'])[0] + "." + str(player['mmr'])[1] + "k" ]
                    for s in mmr_strings:
                        if not s in keywords['keywords']:
                            keywords['keywords'].append(s)
            
            # player races for matchup strings            
            races = teams[player['team_id']] if player['team_id'] in teams.keys() else []
            races.append(player['race'][0])
            teams[player['team_id']] = races
        
        # process the teams array
        for team in teams:    
            teams[team] = {
                'races':   [''.join(i) for i in permutations(teams[team], len(teams[team]))],
                'players': str(len(teams[team]))
            }
        
        # grab the matchup strings
        for i in teams:
            for j in teams:
                if i != j:
                    for matchup_i in teams[i]['races']:
                        for matchup_j in teams[j]['races']:
                            # yep thats 4 for loops
                            tmp = matchup_i + "v" + matchup_j
                            if not tmp in keywords['keywords']:
                                keywords['keywords'].append(tmp)
                    tmp = teams[i]['players'] + "v" + teams[j]['players']
                    if not tmp in keywords['keywords']:
                        keywords['keywords'].append(tmp)
        
        return keywords