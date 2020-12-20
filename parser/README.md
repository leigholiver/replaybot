## replaybot_parser

the "replay" in replaybot

#### `GET /ping`
returns pong if everything is ok

#### `POST /`
`@param url` the replay url to retrieve

`sudo docker build -t replaybot_parser .`

`sudo docker run --rm -p8119:80 --name replaybot_parser replaybot_parser`

example output:
```{
    "duration": "18m38s",
    "map":      "Triton LE",
    "map_hash": "757d1071a3408c716b1c68b1aea4cf645391ae18d9ea48819161723566aa3908"
    "timeUTC":  1580580481469,
    "players": [
        {
            "clan":        "CoolClan",
            "team_id":     1,
            "race":        "Protoss",
            "name":        "LiteralChamp",
            "result":      "Win",
            "apm":         145,
            "profile_url": "https://starcraft2.com/en-gb/profile/2/1/45674357",
            "mmr":         3198,
            color:         {"r": 28, "g": 167, "b": 234, "a": 255, "name": "Teal"}
            is_ai:         false,
            is_random:     false
        },
        {
            "clan":        "",
            "team_id":     2,
            "race":        "Terran",
            "name":        "LosingPlayer",
            "result":      "Loss",
            "apm":         402,
            "profile_url": "https://starcraft2.com/en-gb/profile/2/1/236523236",
            "mmr":         2351,
            color:         {"r": 28, "g": 167, "b": 234, "a": 255, "name": "Teal"}
            is_ai:         false,
            is_random:     false
        },
    ]
}
``` 