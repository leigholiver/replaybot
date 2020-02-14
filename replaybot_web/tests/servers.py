import uuid
from support.lamb.Test import Test
from models.server import server

class servers(Test):
    name = "servers"
    
    def run(self):
        test_server = None
        test_server_id = str(uuid.uuid4())

        self.header("create server test")
        result = True
        try:
            test_server = server(test_server_id)
        except Exception as e:
            print(e)
            self.fail("Couldn't create server, test cannot continue.")
            return

        self.record(result, "[server object]", test_server.data)


        self.header("join server test")
        joined_state = join_event_created = False
        try:
            test_server.join()
            joined_state = test_server.joined
            join_event_created = len(test_server.events) == 1
        except Exception as e:
            print(e)
        self.record(joined_state and join_event_created, "joined_state and join_event_created", str(joined_state) + " and " + str(join_event_created))


        self.header("leave server test")
        left_state = leave_event_created = False
        try:
            test_server.leave()
            left_state = test_server.joined == False
            leave_event_created = len(test_server.events) == 2
        except Exception as e:
            print(e)
        self.record(left_state and leave_event_created, "left_state and leave_event_created", str(left_state) + " and " + str(leave_event_created))


        self.header("save server test")
        result = True
        print(test_server.data)
        try:
            test_server.save()
        except Exception as e:
            print(e)
            result = False
        self.record(result, "True", result)

        self.header("get server test")
        result = True
        try:
            test_b = server.get(test_server_id)
            result = test_b.id == test_server_id 
        except Exception as e:
            print(e)
            result = False
        self.record(result, "True", result)

        test_server.delete()

        return self.successful