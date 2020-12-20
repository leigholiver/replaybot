import http.server, socketserver, json
from io import BytesIO
PORT = 8119

class ServerHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        output = json.dumps({
            "map": "New Repugnancy LE",
            "timeUTC": 132072668902731193,
            "duration": "14m24s",
            "players": [
                {
                    "clan": None,
                    "team_id": 0,
                    "race": "Zerg",
                    "name": "llllllllllll",
                    "result": "Loss",
                    "apm": 312,
                    "profile_url": "https://starcraft2.com/en-gb/profile/1/1/20790392",
                    "mmr": 5031
                },
                {
                    "clan": None,
                    "team_id": 1,
                    "race": "Protoss",
                    "name": "IIIIIIIIIIII",
                    "result": "Win",
                    "apm": 183,
                    "profile_url": "https://starcraft2.com/en-gb/profile/1/1/4353824",
                    "mmr": 5919
                }
            ]
        })

        message = str.encode(output)
        response = BytesIO()
        response.write(message)
        self.wfile.write(response.getvalue())

httpd = socketserver.TCPServer(("0.0.0.0", PORT), ServerHandler)
print("serving at port", PORT)
httpd.serve_forever()