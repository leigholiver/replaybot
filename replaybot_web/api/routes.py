##
# {
#     methods: [ "GET" and/or "POST" ]
#     action: ControllerClass.function
#     middleware: [] # array of middleware class names to apply to the route
# }
# if you update this file, you must run ./lambctl make routes
##
routes = {
    "/discord-code": { 
        "methods": [ "POST" ],
        "action": "discord.exchange_code",
        "middleware": []
    },
    "/servers/(id)/joined": { 
        "methods": [ "GET" ],
        "action": "server_controller.get_server_joined",
        "middleware": []
    },
    "/servers/(id)": { 
        "methods": [ "GET" ],
        "action": "server_controller.get_server",
        "middleware": []
    },
    "/servers/(id)/edit": { 
        "methods": [ "POST" ],
        "action": "server_controller.set_server",
        "middleware": []
    },
    "/servers/(id)/store": { 
        "methods": [ "POST" ],
        "action": "server_controller.store_replay",
        "middleware": [ "hasbottoken" ]
    },
    "/guilds/(guild)/channels": { 
        "methods": [ "GET" ],
        "action": "discord.get_guild_channels",
        "middleware": []
    },
    "/join/(id)": { 
        "methods": [ "POST" ],
        "action": "server_controller.join",
        "middleware": [ "hasbottoken" ]
    },
    "/leave/(id)": { 
        "methods": [ "POST" ],
        "action": "server_controller.leave",
        "middleware": [ "hasbottoken" ]
    },
    "/ping": { 
        "methods": [ "GET", "POST" ],
        "action": "default.ping",
        "middleware": []
    }
}