import mpyq, sc2reader, json, datetime

def parse_replay(filename):
    replay      = sc2reader.load_replay(filename, debug=True)
    archive     = mpyq.MPQArchive(filename)
    replay_data = json.loads(archive.read_file("replay.gamemetadata.json").decode("utf-8"))
    player_meta = {}
    for player in replay_data['Players']:
        player_meta[player["PlayerID"]] = player
    
    players = list()
    for team in replay.teams:
        for player in team.players:
            players.append({
                "team_id":     team.number, 
                "clan":        getattr(player, "clan_tag", None),
                "name":        getattr(player, "name", None),
                "race":        getattr(player, "play_race", None),
                "result":      player_meta[getattr(player, "pid", None)]['Result'] if 'Result' in player_meta[getattr(player, "pid", None)].keys() else 0,
                "profile_url": getattr(player, "url", None),
                "apm":         player_meta[getattr(player, "pid", None)]['APM'] if 'APM' in player_meta[getattr(player, "pid", None)].keys() else 0,
                "mmr":         player_meta[getattr(player, "pid", None)]['MMR'] if 'MMR' in player_meta[getattr(player, "pid", None)].keys() else 0,
                "color":       player.color.__dict__ if hasattr(player, "color") else None,
                "is_ai":       str(player.__class__) == "<class 'sc2reader.objects.Computer'>",
                "is_random":   getattr(player, "pick_race", None) == "Random"
            })

    # todo: should be the minimap image - but doesn't appear in any replays i have?
    # "map_image": archive.read_file('Minimap.tga')

    return {
        "timeUTC":  getattr(replay, "unix_timestamp", None),
        "map": getattr(replay, "map_name", None),
        "map_hash": getattr(replay, "map_hash", None), 
        "duration": duration(replay.real_length.seconds),
        "players":  players
    }

def duration(secs):
    h, m, s = str(datetime.timedelta(seconds=secs)).split(":")
    duration  =  h + "h" if int(h) > 0 else ""
    duration  += m + "m" if int(m) > 0 else ""
    duration  += s + "s" if int(s) > 0 else ""
    return duration