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

        # Reads the inventory and gets volume for each beer.
        (inventory_list, red_helles_volume, pilsner_volume,
         dunkel_volume) = self.read_inventory()

        # Connects 'Add to Inventory' button to add inventory volume.
        self.btn_add_inv.clicked.connect(lambda: self.add_inventory(
            inventory_list))
        # Connects 'Remove from Inventory' button to remove inventory volume.
        self.btn_remove_inv.clicked.connect(lambda: self.remove_inventory(
            inventory_list))

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
            "Organic Red Helles - " + str(red_helles_volume) + " L / " +
            str(red_helles_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Pilsner.
        pilsner_quantity = int(pilsner_volume / 0.5)
        self.lbl_pilsner_inv.setText(
            "Organic Pilsner - " + str(pilsner_volume) + " L / " +
            str(pilsner_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Dunkel.
        dunkel_quantity = int(dunkel_volume / 0.5)
        self.lbl_dunkel_inv.setText(
            "Organic Dunkel - " + str(dunkel_volume) + " L / " +
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

        # Removes inputted volume to the selected beer.
        for inventory in inventory_list:
            if inventory["recipe"] == remove_beer:
                inventory["volume"] -= int(remove_volume)

        # Saves the new inventory to the JSON file.
        self.save_inventory(inventory_list)
        # Updates the volumes in the inventory in the UI.
        self.update_inventory()
