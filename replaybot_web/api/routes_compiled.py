# this file is managed by lamb. any changes to it will be lost.
routes = {
    "GET": [
        {
            "action": "server.get_server_joined",
            "middleware": [],
            "path": "\\/servers\\/(?P<id>.*?)\\/joined\\/?$"
        },
        {
            "action": "server.get_server",
            "middleware": [],
            "path": "\\/servers\\/(?P<id>.*?)\\/?$"
        },
        {
            "action": "discord.get_guild_channels",
            "middleware": [],
            "path": "\\/guilds\\/(?P<guild>.*?)\\/channels\\/?$"
        },
        {
            "action": "default.ping",
            "middleware": [],
            "path": "\\/ping\\/?$"
        }
    ],
    "POST": [
        {
            "action": "discord.exchange_code",
            "middleware": [],
            "path": "\\/discord-code\\/?$"
        },
        {
            "action": "server.set_server",
            "middleware": [],
            "path": "\\/servers\\/(?P<id>.*?)\\/edit\\/?$"
        },
        {
            "action": "server.store_replay",
            "middleware": [
                "hasbottoken"
            ],
            "path": "\\/servers\\/(?P<id>.*?)\\/store\\/?$"
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