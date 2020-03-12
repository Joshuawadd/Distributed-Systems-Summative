import Pyro4
import requests


@Pyro4.expose
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
        return cost

    def list_items(self):
        return food


food = {"Chips": 2, "Pizza": 5, "Burger": 4, "Garlic Bread": 3,
        "Kebab": 3, "Coke": 1, "Chicken Wings": 3.50, "Pasta": 4.50}

order_dict = {1: {"PostCode": "CM9 6BA", "Name": "Sara Ryder", "Order": ["Chips", "Burger", "Garlic Bread"], "Cost": 9},
              2: {"PostCode": "SN1 4JQ", "Name": "James Thompson", "Order": ["Kebab", "Coke", "Garlic Bread", "Chicken Wings"], "Cost": 10.50},
              3: {"PostCode": "DH1 3DF", "Name": "John Smith", "Order": ["Chips", "Pasta"], "Cost": 6.50},
              4: {"PostCode": "DH1 3DF", "Name": "Jane Smith", "Order": ["Chips", "Pasta", "Kebab", "Pizza"], "Cost": 14.50}
              }


def main():
    Pyro4.Daemon.serveSimple(
        {
            Backend: "server.backend"
        },
        ns=True)


if __name__ == "__main__":
    main()
