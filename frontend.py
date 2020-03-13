import Pyro4
import sys
sys.excepthook = Pyro4.util.excepthook


@Pyro4.expose
class FrontEnd(object):
    def check_post_code(self, post_code):
        backend = Pyro4.Proxy("PYRONAME:server.backend.main")
        return (backend.validate_post_code(post_code))

    def list_orders(self, post_code):
        backend = Pyro4.Proxy("PYRONAME:server.backend.main")
        order_list = (backend.get_orders(post_code))
        text = "Here are the previous orders to " + post_code + ": \n"
        for order in order_list:
            text = text + "Name: " + order["Name"] + ". Items: "
            first = True
            for item in order["Order"]:
                if first:
                    text = text + item
                    first = False
                else:
                    text = text + ", " + item
            text = text + ". Cost: " + "£%.2f" % order["Cost"] + "\n"
        return text

    def create_order(self, name, order, post_code):
        backend = Pyro4.Proxy("PYRONAME:server.backend.main")
        item_list = backend.list_items()
        item_list_lower = map(str.lower, item_list)
        for item in order:
            if item.lower() not in item_list_lower:
                return "This is not a valid order."
        details = {"PostCode": post_code, "Name": name, "Order": order}
        cost = backend.new_order(details)
        return "The order has been complete. The total cost will be" + " £%.2f" % cost

    def get_items(self):
        backend = Pyro4.Proxy("PYRONAME:server.backend.main")
        item_list = backend.list_items()
        text = "Here is the list of items: "
        for item in item_list:
            text = text + item + ", "
        return text


def main():
    daemon = Pyro4.Daemon()
    uri = daemon.register(FrontEnd)
    ns.register("server.frontend", uri)

    print("Ready on server.frontend")
    daemon.requestLoop()

    ns.remove(name="server.frontend")


if __name__ == "__main__":
    ns = Pyro4.locateNS()
    main()
