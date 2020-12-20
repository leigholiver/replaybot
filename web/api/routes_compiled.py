# this file is managed by lamb. any changes to it will be lost.
routes = {
    "GET": [
        {
            "action": "discord.exchange_code",
            "middleware": [],
            "path": "\\/discord\\/?$"
        },
        {
            "action": "server.user_servers",
            "middleware": [
                "auth"
            ],
            "path": "\\/user-servers\\/?$"
        },
        {
            "action": "server.get_server",
            "middleware": [],
            "path": "\\/servers\\/(?P<id>.*?)\\/?$"
        },
        {
            "action": "replays.list",
            "middleware": [
                "auth"
            ],
            "path": "\\/replays\\/list\\/?$"
        },
        {
            "action": "replays.search",
            "middleware": [
                "auth"
            ],
            "path": "\\/replays\\/search\\/?$"
        },
        {
            "action": "default.ping",
            "middleware": [],
            "path": "\\/ping\\/?$"
        }
    ],
    "POST": [
        {
            "action": "server.set_server",
            "middleware": [
                "auth"
            ],
            "path": "\\/servers\\/(?P<id>.*?)\\/edit\\/?$"
        },
        {
            "action": "replays.store",
            "middleware": [
                "hasbottoken"
            ],
            "path": "\\/store-replay\\/?$"
        },
        {
            "action": "server.join",
            "middleware": [
                "hasbottoken"
            ],
            "path": "\\/join\\/(?P<id>.*?)\\/?$"
        },
        {
            "action": "server.leave",
            "middleware": [
                "hasbottoken"
            ],
            "path": "\\/leave\\/(?P<id>.*?)\\/?$"
        },
        {
            "action": "default.ping",
            "middleware": [],
            "path": "\\/ping\\/?$"
        }
    ]
}