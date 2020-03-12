import Pyro4

@Pyro4.expose
class GetName(object):
    def get_fortune(self, name):
        return greeting_maker = Pyro4.Proxy("PYRONAME:server.backendend")
                (greeting_maker.get_fortune(name))

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GreetingMaker)   # register the greeting maker as a Pyro object
ns.register("server.frontend", uri)   # register the object with a name in the name server



print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls