# saved as greeting-client.py
import Pyro4
import sys
sys.excepthook = Pyro4.util.excepthook

# use name server object lookup uri shortcut
server = Pyro4.Proxy("PYRONAME:server.frontend")

another_order = True

while another_order:
    post_code = input(
        "Hello! Welcome to the Just Hungry takeaway ordering service. Please enter your postcode:").strip()
    while server.check_post_code(post_code.upper()) == False:
        post_code = input("Please enter a valid UK postcode:").strip()

    post_code = post_code.upper()

    print(server.list_orders(post_code))
    name = input("Please enter your name: ").strip()
    print(server.get_items())

    order = []
    item = input("Please enter an item: ").strip()
    while item != "End":
        order.append(item)
        item = input(
            "Please enter an item, or type 'End' to end your order: ").strip()

    if order:
        print(server.create_order(name, order, post_code))

    cont = input("Would you like to place another order? (Y/N) ").strip()
    while cont.upper() != "Y" and cont.upper() != "N":
        cont = input("Would you like to place another order? (Y/N) ").strip()

    if cont.upper() == "N":
        another_order = False

print("Thank you for using Just Hungry. We hope you use the service again.")
