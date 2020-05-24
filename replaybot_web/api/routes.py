##
# {
#     methods: [ "GET" and/or "POST" ]
#     action: controller_class.function
#     middleware: [] # array of middleware class names to apply to the route
# }
##
routes = {
    "/discord-code": { 
        "methods": [ "POST" ],
        "action": "discord.exchange_code",
        "middleware": []
    },
    "/servers/(id)/joined": { 
        "methods": [ "GET" ],
        "action": "server.get_server_joined",
        "middleware": []
    },
    "/servers/(id)": { 
        "methods": [ "GET" ],
        "action": "server.get_server",
        "middleware": []
    },
    "/servers/(id)/edit": { 
        "methods": [ "POST" ],
        "action": "server.set_server",
        "middleware": []
    },
    "/servers/(id)/store": { 
        "methods": [ "POST" ],
        "action": "server.store_replay",
        "middleware": [ "hasbottoken" ]
    },
    "/guilds/(guild)/channels": { 
        "methods": [ "GET" ],
        "action": "discord.get_guild_channels",
        "middleware": []
    },
    "/join/(id)": { 
        "methods": [ "POST" ],
        "action": "server.join",
        "middleware": [ "hasbottoken" ]
    },
    "/leave/(id)": { 
        "methods": [ "POST" ],
        "action": "server.leave",
        "middleware": [ "hasbottoken" ]
    },
    "/ping": { 
        "methods": [ "GET", "POST" ],
        "action": "default.ping",
        "middleware": []
    }
}