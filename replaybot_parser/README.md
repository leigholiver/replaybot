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
    "map": "Imperio eterno EE",
    "timeUTC": 1580580481469,
    "players": [
        {
            "clan": "GeekA",
            "team_id": 0,
            "race": "Protoss",
            "name": "DarthJulius",
            "result": "Win",
            "apm": 145,
            "profile_url": "https://starcraft2.com/en-gb/profile/2/1/8886",
            "mmr": 3198
        },
        {
            "clan": "GeekA",
            "team_id": 1,
            "race": "Terran",
            "name": "Oconor",
            "result": "Loss",
            "apm": 114,
            "profile_url": "https://starcraft2.com/en-gb/profile/1/1/7281766",
            "mmr": 2793
        }
    ]
}
```