import sys, os, json, mpyq, requests, uuid, datetime
from flask import Flask, Response, request
from s2protocol import versions

app = Flask(__name__)

@app.route('/ping', methods=["GET"])
def ping():
    return "pong"

@app.route('/', methods=["POST"])
def parse():
    filename = "/tmp/" + str(uuid.uuid4())
    content = request.json

    try:
        url = content['url']
    except:
        return Response(400)

    try:
        # download the replay to temp file
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)

        # load it
        archive = mpyq.MPQArchive(filename)
        contents = archive.header['user_data_header']['content']
        header = versions.latest().decode_replay_header(contents)
        baseBuild = header['m_version']['m_baseBuild']
        
        try:
            protocol = versions.build(baseBuild)
        except:
            # Todo: Alert on this so we can update the protocol
            pass

        # get the details
        contents = archive.read_file('replay.details')
        details = protocol.decode_replay_details(contents)

        # get the metadata
        contents = archive.read_file('replay.gamemetadata.json')
        metadata = json.loads(contents)
        
        # Duration
        if header['m_useScaledTime']: # lotv time
            s = int(header['m_elapsedGameLoops']/1.4/16) # rando numbers from blizzard entertainment
        else: # hots time, as rare as that will be, if ever
            s = int(header['m_elapsedGameLoops']/16)
        
        h, m, s = str(datetime.timedelta(seconds=s)).split(":")
        duration  =  h + "h" if int(h) > 0 else ""
        duration  += m + "m" if int(m) > 0 else ""
        duration  += s + "s" if int(s) > 0 else ""

        try:
            # Map image
            minimap = archive.read_file('Minimap.tga')
            with open("/tmp/Minimap.tga", 'wb') as f:
                f.write(minimap)
        except Exception as e:
            print(e)

        out = {
            "map": details['m_title'],
            "timeUTC": details['m_timeUTC']/10000-11644473600000, # more rando magic numbers from blizzard entertainment
            "duration": duration
        }

        players = []

        for i in range(0, len(details['m_playerList'])):
            if details['m_playerList'][i]['m_observe'] == 0:

                # process the name
                name = details['m_playerList'][i]['m_name'].split("<sp/>")
                if len(name) > 1:
                    clan = name[0].replace("&lt;", "").replace("&gt;", "")
                    name = name[1]
                else:
                    clan = None
                    name = name[0]
                # process the profile url from m_toon
                profile_url = "https://starcraft2.com/en-gb/profile/"
                profile_url += str(details['m_playerList'][i]['m_toon']['m_realm']) + "/"
                profile_url += str(details['m_playerList'][i]['m_toon']['m_region']) + "/"
                profile_url += str(details['m_playerList'][i]['m_toon']['m_id'])
                
                mmr = 0
                if 'MMR' in metadata['Players'][i].keys():
                    mmr = metadata['Players'][i]['MMR']
                                    
                players.append({
                    "team_id": details['m_playerList'][i]['m_teamId'],
                    "race": details['m_playerList'][i]['m_race'],
                    "clan": clan,
                    "name": name,
                    "profile_url": profile_url,
                    "mmr": mmr,
                    "result": metadata['Players'][i]['Result'],
                    "apm": metadata['Players'][i]['APM']
                })

        out['players'] = players

        # remove the temp file
        # should probably do this on a cron instead of every request
        os.remove(filename)

        return Response(response=json.dumps(out),
                    status=200,
                    mimetype="application/json")
    except:
        return Response(500)

    return Response(400)

if __name__ == '__main__':
    app.run(debug = True, host='0.0.0.0')