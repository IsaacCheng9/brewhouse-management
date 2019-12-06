"""
A system to manage the inventory of Barnaby's Brewhouse, allowing the user to
add or remove volumes of each type of beer, and calculating the overall volume
and number of bottles of each beer.
"""

import json
from typing import Tuple

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from inv_management_setup import Ui_dialog_inv_management


class InventoryManagementDialog(QDialog, Ui_dialog_inv_management):
    """Contains the dialog window for inventory management."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts volume input to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_update_inv_volume.setValidator(self.only_int)
        self.line_edit_add_order_volume.setValidator(self.only_int)

        # Reads the inventory and gets volume for each beer.
        (inventory_list, red_helles_volume, pilsner_volume,
         dunkel_volume) = self.read_inventory()
        # Reads the customer order list and adds to UI..
        order_list = self.read_orders()

        # Connects 'Add to Inventory' button to add inventory volume.
        self.btn_add_inv.clicked.connect(lambda: self.add_inventory(
            inventory_list))
        # Connects 'Remove from Inventory' button to remove inventory volume.
        self.btn_remove_inv.clicked.connect(lambda: self.remove_inventory(
            inventory_list))
        # Connects 'Add Order' button to add customer order.
        self.btn_add_order.clicked.connect(lambda: self.add_order(order_list))
        # Connects 'Dispatch Order' button to dispatch customer order.
        self.btn_dispatch_order.clicked.connect(lambda: self.dispatch_order(
            inventory_list, order_list))

        # Updates the volumes in the inventory in the UI.
        self.update_inventory()

    def read_inventory(self) -> Tuple[list, int, int, int]:
        """Reads the JSON file for inventory and gets volume for each beer.

        Returns:
            inventory_list (list): List storing the volume for each beer.
            red_helles_volume (int): Volume (L) of Red Helles.
            pilsner_volume (int): Volume (L) of Pilsner.
            dunkel_volume (int): Volume (L) of Dunkel.
        """
        with open("inventory.json", "r") as inventory_file:
            try:
                inventory_list = json.load(inventory_file)
                for inventory in inventory_list:
                    if inventory["recipe"] == "red_helles":
                        red_helles_volume = int(inventory["volume"])
                    elif inventory["recipe"] == "pilsner":
                        pilsner_volume = int(inventory["volume"])
                    elif inventory["recipe"] == "dunkel":
                        dunkel_volume = int(inventory["volume"])
            except ValueError:
                print("Empty JSON file.")

        return inventory_list, red_helles_volume, pilsner_volume, dunkel_volume

    def update_inventory(self):
        """Updates the volumes in the inventory in the UI."""
        (inventory_list, red_helles_volume, pilsner_volume,
         dunkel_volume) = self.read_inventory()

        # Shows the volume and number of bottles of Red Helles.
        red_helles_quantity = int(red_helles_volume / 0.5)
        self.lbl_red_helles_inv.setText(
            "Organic Red Helles: " + str(red_helles_volume) + " L / " +
            str(red_helles_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Pilsner.
        pilsner_quantity = int(pilsner_volume / 0.5)
        self.lbl_pilsner_inv.setText(
            "Organic Pilsner: " + str(pilsner_volume) + " L / " +
            str(pilsner_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Dunkel.
        dunkel_quantity = int(dunkel_volume / 0.5)
        self.lbl_dunkel_inv.setText(
            "Organic Dunkel: " + str(dunkel_volume) + " L / " +
            str(dunkel_quantity) + " bottle(s)")

    def save_inventory(self, inventory_list: list):
        """Saves the new inventory to the JSON file.

        Args:
            inventory_list (list): List storing the volume for each beer.
        """
        with open("inventory.json", "w") as inventory_file:
            json.dump(inventory_list, inventory_file,
                      ensure_ascii=False, indent=4)

    def add_inventory(self, inventory_list: list):
        """Adds the given volume to the given beer in the inventory.

        Args:
            inventory_list (list): List storing the volume for each beer.
        """
        # Gets the beer and volume inputs.
        add_beer_input = self.combo_box_update_inv_recipe.currentText()
        if add_beer_input == "Organic Red Helles":
            add_beer = "red_helles"
        elif add_beer_input == "Organic Pilsner":
            add_beer = "pilsner"
        elif add_beer_input == "Organic Dunkel":
            add_beer = "dunkel"
        add_volume = self.line_edit_update_inv_volume.text()

        # Validates against null input.
        if add_volume != "":
            # Adds inputted volume to the selected beer.
            for inventory in inventory_list:
                if inventory["recipe"] == add_beer:
                    inventory["volume"] += int(add_volume)

            # Saves the new inventory to the JSON file.
            self.save_inventory(inventory_list)
            # Updates the volumes in the inventory in the UI.
            self.update_inventory()

    def remove_inventory(self, inventory_list: list):
        """Removes the given volume to the given beer in the inventory.

        Args:
            inventory_list (list): List storing the volume for each beer.
        """
        # Gets the beer and volume inputs.
        remove_beer_input = self.combo_box_update_inv_recipe.currentText()
        if remove_beer_input == "Organic Red Helles":
            remove_beer = "red_helles"
        elif remove_beer_input == "Organic Pilsner":
            remove_beer = "pilsner"
        elif remove_beer_input == "Organic Dunkel":
            remove_beer = "dunkel"
        remove_volume = self.line_edit_update_inv_volume.text()

        # Validates against null input.
        if remove_volume != "":
            # Removes inputted volume to the selected beer.
            for inventory in inventory_list:
                if inventory["recipe"] == remove_beer:
                    inventory["volume"] -= int(remove_volume)

            # Saves the new inventory to the JSON file.
            self.save_inventory(inventory_list)
            # Updates the volumes in the inventory in the UI.
            self.update_inventory()

    def read_orders(self) -> list:
        """Reads the customer orders from the JSON file and adds to UI.

        Returns:
            order_list (list): A list of the customer orders.
        """
        display_orders = ""

        with open("customer_orders.json", "r") as orders_file:
            try:
                order_list = json.load(orders_file)
            except ValueError:
                print("Empty JSON file")

        # Iterates through the orders and adds their details to an order list.
        for order in order_list:
            display_orders += ("Order ID: " + order["order_id"] + ", Beer "
                               "Recipe: " + order["order_recipe"] +
                               ", Order Volume: " +
                               str(order["order_volume"]) + "\n")

        # Displays list of orders in UI.
        self.lbl_orders.setText(display_orders.rstrip())

        return order_list

    def save_orders(self, order_list: list):
        """Saves order list to JSON file.

        Args:
            order_list (list): A list of the customer orders.
        """
        with open("customer_orders.json", "w") as orders_file:
            json.dump(order_list, orders_file,
                      ensure_ascii=False, indent=4)

    def add_order(self, order_list: list):
        """Adds customer order to the list.

        Args:
            order_list (list): A list of the customer orders.
        """

        # Gets the inputs for the new customer order.
        try:
            order_id = self.line_edit_add_order_id.text()
            order_recipe = self.combo_box_add_order_recipe.currentText()
            order_volume = int(self.line_edit_add_order_volume.text())
        except (ValueError, TypeError):
            pass

        # Validates against null inputs.
        if order_id != "" and str(order_volume) != "":
            # Appends order to order list.
            order = {"order_id": order_id,
                     "order_recipe": order_recipe,
                     "order_volume": order_volume}
            order_list.append(order)

            # Saves order list to JSON file.
            self.save_orders(order_list)

            # Displays message to confirm their new order was added.
            self.lbl_order_message.setText("Order added successfully.")

            # Updates orders list in UI.
            self.read_orders()
        else:
            # Displays message to notify their new order was unsuccessful.
            self.lbl_order_message.setText("This is not a valid order to add. "
                                           "Please add input in all fields.")

    def dispatch_order(self, inventory_list: list, order_list: list):
        """Dispatches customer order from the list.

        Args:
            inventory_list (list): List storing the volume for each beer.
            order_list (list): A list of the customer orders.
        """

        try:
            dispatch_order_id = self.line_edit_dispatch_order_id.text()
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if dispatch_order_id != "":
            # Checks for the order in the order list.
            for order in order_list:
                if dispatch_order_id == order["order_id"]:
                    for inventory in inventory_list:
                        # Subtracts volume of beer from order from inventory.
                        if ((order["order_recipe"] == "Organic Red Helles" and
                             inventory["recipe"] == "red_helles")
                                or
                                (order["order_recipe"] == "Organic Pilsner" and
                                 inventory["recipe"] == "pilsner")
                                or
                                (order["order_recipe"] == "Organic Dunkel" and
                                 inventory["recipe"] == "dunkel")):
                            inventory["volume"] -= order["order_volume"]

                    # Removes order from the order list.
                    order_list.remove(order)

                    # Saves order list to JSON file.
                    self.save_orders(order_list)
                    # Displays message to say dispatch was successful.
                    self.lbl_order_message.setText("Order dispatched "
                                                   "successfully.")
                    # Updates orders list in UI.
                    self.read_orders()
                    # Saves the new inventory to the JSON file.
                    self.save_inventory(inventory_list)
                    # Updates the volumes in the inventory in the UI.
                    self.update_inventory()
        else:
            # Displays message to say dispatch was unsuccessful.
            self.lbl_order_message.setText("This is not a valid order to "
                                           "dispatch. Please input the order "
                                           "ID.")
