class route_util():
    def compile_routes(self, routes):
        output = {}
        for route in routes.keys():
            obj = {
                "path": self.compile(route),
                "action": routes[route]['action'],
                "middleware": routes[route]['middleware']
            }

            for method in routes[route]['methods']:
                if method in output.keys():
                    output[method].append(obj)
                else:
                    output[method] = [obj]
        return output

    def compile(self, route):
        tmp = route.replace("/", "\\/")
        tmp = tmp.replace("(", "(?P<")
        tmp = tmp.replace(")", ">.*?)")
        if not tmp.endswith("/"):
            tmp += "\\/?"   
        tmp += "$"
        return tmp