##
# {
#     methods: [ "GET" and/or "POST" ]
#     action: controller_class.function
#     middleware: [] # array of middleware class names to apply to the route
# }
##
routes = {
    #  redirect uri for discord
    "/discord": { 
        "methods": [ "GET" ],
        "action": "discord.exchange_code",
        "middleware": []
    },

    # get joined status for logged in users servers
    "/user-servers": { 
        "methods": [ "GET" ],
        "action": "server.user_servers",
        "middleware": ["auth"]
    },

    # get server meta/config
    "/servers/(id)": { 
        "methods": [ "GET" ],
        "action": "server.get_server",
        "middleware": []
        # hey dont put the auth middleware here, its handled in the controller
        # todo: refactor into a bot-or-auth middleware
    },

    # set server config
    "/servers/(id)/edit": { 
        "methods": [ "POST" ],
        "action": "server.set_server",
        "middleware": ["auth"]
    },

    # store a replay
    "/store-replay": { 
        "methods": [ "POST" ],
        "action": "replays.store",
        "middleware": [ "hasbottoken" ]
    },

    # replay list/search
    "/replays/list": { 
        "methods": [ "GET" ],
        "action": "replays.list",
        "middleware": ["auth"]
    },
    "/replays/search": { 
        "methods": [ "GET" ],
        "action": "replays.search",
        "middleware": ["auth"]
    },

    # bot api endpoints for join/leave events
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

    # healthcheck
    "/ping": { 
        "methods": [ "GET", "POST" ],
        "action": "default.ping",
        "middleware": []
    }
}