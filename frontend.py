import Pyro4


@Pyro4.expose
class FrontEnd(object):
    def check_post_code(self, post_code):
        return (backend.validate_post_code(post_code))

    def list_orders(self, post_code):
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
        item_list = backend.list_items()
        for item in order:
            if item not in item_list:
                return "This is not a valid order."
        details = {"PostCode": post_code, "Name": name, "Order": order}
        cost = backend.new_order(details)
        return "The order has been complete. The total cost will be" + " £%.2f" % cost

    def get_items(self):
        item_list = backend.list_items()
        text = "Here is the list of items: "
        for item in item_list:
            text = text + item + ", "
        return text


def main():
    Pyro4.Daemon.serveSimple(
        {
            FrontEnd: "server.frontend"
        },
        ns=True)


if __name__ == "__main__":
    backend = Pyro4.Proxy("PYRONAME:server.backend")
    main()
