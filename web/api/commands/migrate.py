import json
from framework.lamb.command import command
from models.server import server as m_server
from models.replay import replay as m_replay

class migrate(command):
    servers_path = "migration/servers.json"
    replays_path = "migration/replays.json"

    def run(self, data):

        with open(self.servers_path) as server_file:
            servers = json.load(server_file)
            print("found %d servers" % len(servers))
            for server in servers:
                if server['joined']:
                    s = m_server()
                    s.id      = server['id'] if 'id' in server.keys() else ""
                    s.joined  = server['joined'] if 'joined' in server.keys() else ""
                    s.replyTo = server['replyTo'] if 'replyTo' in server.keys() else ""
                    s.listen  = server['listen'] if 'listen' in server.keys() else ""
                    s.exclude = server['exclude'] if 'exclude' in server.keys() else ""
                    s.name    = server['name'] if 'name' in server.keys() else ""
                    s.icon    = server['icon'] if 'icon' in server.keys() else ""
                    s.save()
                    print("saved %s" % server['id'])

        with open(self.replays_path) as rep_file:
            replays = json.load(rep_file)
            print("found %d replays" % len(replays))
            for replay in replays:
                r = m_replay()
                r.id    = replay['id']
                r.guild = replay['guild']
                r.replay_data = replay['replay_data']
                r.save()
                print("saved %s" % replay['id'])
