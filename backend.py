import Pyro4
import requests
import sys
sys.excepthook = Pyro4.util.excepthook

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Backend(object):
    def validate_post_code(self, post_code):
        response = requests.get(
            "http://api.postcodes.io/postcodes/" + post_code + "/validate")
        data = response.json()
        return data["result"]

    def get_orders(self, post_code):
        order_list = []
        for orders in order_dict:
            if order_dict[orders]["PostCode"] == post_code:
                order_list.append(order_dict[orders])
        return order_list

    def new_order(self, details):
        cost = 0
        for item in details["Order"]:
            cost = cost + food[item]
        details["Cost"] = cost
        order_dict[len(order_dict)+1] = details
        for backup in ns.list(prefix="server.backend.reserve"):
            reserve = Pyro4.Proxy("PYRONAME:"+backup)
            reserve.update_backups(order_dict)
        return cost

    def list_items(self):
        return food

    def update_backups(self, new_dict):
        order_dict.clear()
        order_dict.update(new_dict)

    def change_to_main(self, backup_name):
        global uri
        ns.remove(name=backup_name)
        ns.register("server.backend.main", uri)
        print("Ready on server.backend.main")


food = {"Chips": 2, "Pizza": 5, "Burger": 4, "Garlic Bread": 3,
        "Kebab": 3, "Coke": 1, "Chicken Wings": 3.50, "Pasta": 4.50}

order_dict = {1: {"PostCode": "CM9 6BA", "Name": "Sara Ryder", "Order": ["Chips", "Burger", "Garlic Bread"], "Cost": 9},
              2: {"PostCode": "SN1 4JQ", "Name": "James Thompson", "Order": ["Kebab", "Coke", "Garlic Bread", "Chicken Wings"], "Cost": 10.50},
              3: {"PostCode": "DH1 3DF", "Name": "John Smith", "Order": ["Chips", "Pasta"], "Cost": 6.50},
              4: {"PostCode": "DH1 3DF", "Name": "Jane Smith", "Order": ["Chips", "Pasta", "Kebab", "Pizza"], "Cost": 14.50}
              }


def main():
    global uri
    if not ns.list(prefix="server.backend.main"):
        server_name = "server.backend.main"
    else:
        server_num = len(ns.list(prefix="server.backend.reserve")) + 1
        server_name = "server.backend.reserve" + str(server_num)
    daemon = Pyro4.Daemon()                # make a Pyro daemon                # find the name server
    uri = daemon.register(Backend)   # register the greeting maker as a Pyro object
    ns.register(server_name, uri)   # register the object with a name in the name server

    print("Ready on " + server_name)
    daemon.requestLoop()


    # if not ns.list(prefix="server.backend.main"):
    #     server_name = "server.backend.main"
    # else:
    #     server_num = len(ns.list(prefix="server.backend.reserve")) + 1
    #     server_name = "server.backend.reserve" + str(server_num)
    # Pyro4.Daemon.serveSimple(
    #     {
    #         Backend: server_name
    #     },
    #     ns=True)
    if not ns.list(prefix="server.backend.reserve"):
        ns.remove(name="server.backend.main")
    else:
        backup_list = list(ns.list(prefix="server.backend.reserve").keys())
        backup = backup_list[0]
        reserve = Pyro4.Proxy("PYRONAME:"+backup)

        ns.remove(name=server_name)
        reserve.change_to_main(backup) 


if __name__ == "__main__":
    uri = ""
    ns = Pyro4.locateNS()
    main()
    
