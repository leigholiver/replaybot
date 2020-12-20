routes = {
    "GET": [
        {
            "action": "testcontroller.hello",
            "middleware": [],
            "path": "\\/hello\\/(?P<name>.*?)\\/?$"
        },
        {
            "action": "testcontroller.ping",
            "middleware": [],
            "path": "\\/ping\\/?$"
        },
        {
            "action": "testcontroller.pong",
            "middleware": [
                "testmiddleware"
            ],
            "path": "\\/pong\\/?$"
        }
    ],
    "POST": [
        {
            "action": "testcontroller.ping",
            "middleware": [],
            "path": "\\/ping\\/?$"
        }
    ]
}