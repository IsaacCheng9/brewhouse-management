"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

import json
import logging
import sys
from datetime import datetime
from time import localtime, strftime, time
from typing import Tuple

import pandas
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMainWindow

from brewhouse_setup import Ui_mwindow_brewhouse
from inv_management_setup import Ui_dialog_inv_management
from process_monitoring_setup import Ui_dialog_monitoring


def main() -> None:
    """Opens the program window, and exits program when window is closed."""
    app = QtWidgets.QApplication(sys.argv)
    setup_logging()
    mwindow_brewhouse = BrewhouseWindow()
    mwindow_brewhouse.show()
    sys.exit(app.exec())


def setup_logging():
    """
    Sets up the logging system to automatically log actions to log file.
    """
    logging.basicConfig(filename="logs.txt", level=logging.DEBUG,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.debug("Barnaby's Brewhouse program started.")


class BrewhouseWindow(QMainWindow, Ui_mwindow_brewhouse):
    """Contains the main window for the Brewhouse application."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Connects 'Inventory Management' button to the inventory dialog.
        self.btn_inv_management.clicked.connect(
            self.open_dialog_inv_management)

        # Connects 'Process Monitoring' button to the monitoring dialog.
        self.btn_process_monitoring.clicked.connect(
            self.open_dialog_monitoring)

        # Reads sales data from the CSV file.
        data_frame = self.read_sales_data()

        # Calculates total sales and sales ratios of beer.
        self.get_sales_ratio(data_frame)

        # Calculates average monthly growth rates in sales of beer.
        (beers, red_helles_growth, pilsner_growth,
         dunkel_growth) = self.get_avg_growth_rate(data_frame)

        # Predicts future sales of a given beer in a given month.
        self.btn_predict.clicked.connect(lambda: self.predict_sales(
            data_frame, red_helles_growth, pilsner_growth, dunkel_growth))

    def open_dialog_inv_management(self) -> None:
        """Opens the dialog for the user to manage inventory."""
        self.Dialog = InventoryManagementDialog()
        self.Dialog.open()

    def open_dialog_monitoring(self) -> None:
        """Opens the dialog for the user to monitor brewing processes."""
        self.Dialog = ProcessMonitoringDialog()
        self.Dialog.open()

    def read_sales_data(self) -> pandas.core.frame.DataFrame:
        """Reads the sales data and loads it to a variable.

        Returns:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.
        """
        data_frame = pandas.read_csv("sales_data.csv")
        print(str(data_frame) + "\n")

        return data_frame

    def get_sales_ratio(self, data_frame:
                        pandas.core.frame.DataFrame):
        """Calculates total sales and sales ratio for different beers.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.
        """
        # Sums the total sales of all beers.
        total_sales = int(data_frame["Quantity ordered"].sum())

        # Sums Red Helles sales and calculates their sales ratio.
        red_helles = data_frame.query("Recipe == 'Organic Red Helles'")
        red_helles_sales = int(red_helles["Quantity ordered"].sum())
        red_helles_ratio = round((red_helles_sales / total_sales) * 100, 3)

        # Sums Pilsner sales and calculates their sales ratio.
        pilsner = data_frame.query("Recipe == 'Organic Pilsner'")
        pilsner_sales = int(pilsner["Quantity ordered"].sum())
        pilsner_ratio = round((pilsner_sales / total_sales) * 100, 3)

        # Sums Dunkel sales and calculates their sales ratio.
        dunkel = data_frame.query("Recipe == 'Organic Dunkel'")
        dunkel_sales = int(dunkel["Quantity ordered"].sum())
        dunkel_ratio = round((dunkel_sales / total_sales) * 100, 3)

        # Displays the sales and sales ratios of beers in UI.
        self.lbl_overall_sales.setText(
            "Overall - " + str(total_sales))
        self.lbl_red_helles_sales.setText(
            "Organic Red Helles - " + str(red_helles_sales))
        self.lbl_pilsner_sales.setText(
            "Organic Pilsner - " + str(pilsner_sales))
        self.lbl_dunkel_sales.setText(
            "Organic Dunkel - " + str(dunkel_sales))
        self.lbl_red_helles_ratio.setText(
            "Organic Red Helles - " + str(red_helles_ratio) + "%")
        self.lbl_pilsner_ratio.setText(
            "Organic Pilsner - " + str(pilsner_ratio) + "%")
        self.lbl_dunkel_ratio.setText(
            "Organic Dunkel - " + str(dunkel_ratio) + "%")

    def get_avg_growth_rate(self, data_frame:
                            pandas.core.frame.DataFrame) -> Tuple[list, float,
                                                                  float,
                                                                  float]:
        """Calculates the average monthly growth rate from sales data.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.

        Returns:
            beers (list): A list of the beers.
            red_helles_growth (float): Average growth rate of sales for Red
                                       Helles.
            pilsner_growth (float): Average growth rate of sales for Pilsner.
            dunkel_growth (float): Average growth rate of sales for Dunkel.
        """
        # Growth rates for Red Helles, Pilsner, and Dunkel.
        red_helles_growth = float()
        pilsner_growth = float()
        dunkel_growth = float()

        # Sets filters for each month.
        months = ["Nov-18", "Dec-18", "Jan-19", "Feb-19", "Mar-19", "Apr-19",
                  "May-19", "Jun-19", "Jul-19", "Aug-19", "Sep-19", "Oct-19"]
        beers = ["Organic Red Helles", "Organic Pilsner", "Organic Dunkel"]

        # Iterates through monthly sales of each type of beer.
        for beer in beers:
            month_filter_previous = data_frame["Date Required"].str.contains(
                "Nov-18")
            for month in months:
                month_filter_current = (
                    data_frame["Date Required"].str.contains(month))
                beer_filter = data_frame["Recipe"].isin([beer])

                # Filters data to the sales in a month for that type of beer.
                month_data_current = data_frame[month_filter_current &
                                                beer_filter]
                month_data_previous = data_frame[month_filter_previous &
                                                 beer_filter]
                month_sales_current = int(
                    month_data_current["Quantity ordered"].sum())
                month_sales_previous = int(
                    month_data_previous["Quantity ordered"].sum())

                # Accumulates growth rate for each type of beer.
                if beer == "Organic Red Helles" and month != "Nov-18":
                    red_helles_growth += (month_sales_current /
                                          month_sales_previous)
                elif beer == "Organic Pilsner" and month != "Nov-18":
                    pilsner_growth += (month_sales_current /
                                       month_sales_previous)
                elif beer == "Organic Dunkel" and month != "Nov-18":
                    dunkel_growth += (month_sales_current /
                                      month_sales_previous)

                # Updates previous month to enable monthly sales comparisons.
                month_filter_previous = month_filter_current

        # Calculates mean from cumulative growth rates.
        red_helles_growth /= 11
        pilsner_growth /= 11
        dunkel_growth /= 11

        red_helles_growth_pct = round((red_helles_growth - 1) * 100, 3)
        pilsner_growth_pct = round((pilsner_growth - 1) * 100, 3)
        dunkel_growth_pct = round((dunkel_growth - 1) * 100, 3)

        # Displays percentage of sales provided by each beer in UI.
        self.lbl_red_helles_growth.setText(
            "Organic Red Helles - " + str(red_helles_growth_pct) + "%")
        self.lbl_pilsner_growth.setText(
            "Organic Pilsner - " + str(pilsner_growth_pct) + "%")
        self.lbl_dunkel_growth.setText(
            "Organic Dunkel - " + str(dunkel_growth_pct) + "%")

        return beers, red_helles_growth, pilsner_growth, dunkel_growth

    def predict_sales(self, data_frame:
                      pandas.core.frame.DataFrame, red_helles_growth: float,
                      pilsner_growth: float, dunkel_growth: float) -> int:
        """Predicts future sales of Red Helles, Pilsner, and Dunkel.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.
            red_helles_growth (float): Average growth rate of sales for Red
                                       Helles.
            pilsner_growth (float): Average growth rate of sales for Pilsner.
            dunkel_growth (float): Average growth rate of sales for Dunkel.

        Returns:
            prediction_sales (int): Predicted monthly sales of a given beer for
                                    a given month.
        """

        # Gets the date to predict the sales for.
        prediction_date = self.date_edit_predict.text()

        # Calculates number of months since the last month of sales data.
        format_date = "%d/%m/%Y"
        final_date = datetime.strptime("30/10/2019", format_date).date()
        prediction_date = datetime.strptime(
            prediction_date, format_date).date()
        month_difference = ((prediction_date.year - final_date.year) *
                            12 + (prediction_date.month - final_date.month))

        # Filters to last month's sales of Red Helles, Pilsner, and Dunkel.
        last_month_filter = data_frame["Date Required"].str.contains("Oct-19")
        red_helles_filter = data_frame["Recipe"].str.contains(
            "Organic Red Helles")
        pilsner_filter = data_frame["Recipe"].str.contains("Organic Pilsner")
        dunkel_filter = data_frame["Recipe"].str.contains("Organic Dunkel")

        # Gets last month's sales of Red Helles, Pilsner, and Dunkel.
        last_red_helles_data = data_frame[last_month_filter &
                                          red_helles_filter]
        last_pilsner_data = data_frame[last_month_filter & pilsner_filter]
        last_dunkel_data = data_frame[last_month_filter & dunkel_filter]
        last_red_helles_sales = int(
            last_red_helles_data["Quantity ordered"].sum())
        last_pilsner_sales = int(last_pilsner_data["Quantity ordered"].sum())
        last_dunkel_sales = int(last_dunkel_data["Quantity ordered"].sum())

        # Predicts beer sales for given month, rounded down to nearest integer.
        predicted_red_helles_sales = int((last_red_helles_sales *
                                          (red_helles_growth **
                                           month_difference)))
        predicted_pilsner_sales = int((last_pilsner_sales *
                                       (pilsner_growth ** month_difference)))
        predicted_dunkel_sales = int((last_dunkel_sales *
                                      (dunkel_growth ** month_difference)))

        # Shows the calculations of sales predictions for the given date in UI.
        self.lbl_predictions.setText(
            "(Last Monthly Beer Sales * (Average Beer Growth Rate ^ " +
            "Month Difference))\nOrganic Red Helles: (" +
            str(last_red_helles_sales) + " * (" + str(red_helles_growth) +
            " ^ " + str(month_difference) + ")) = " +
            str(predicted_red_helles_sales) +
            "\nOrganic Pilsner: (" + str(last_pilsner_sales) + "* (" +
            str(pilsner_growth) + " ^ " + str(month_difference) + ")) = " +
            str(predicted_pilsner_sales) +
            "\nOrganic Dunkel: (" + str(last_dunkel_sales) + "* (" +
            str(dunkel_growth) + " ^ " + str(month_difference) + ")) = " +
            str(predicted_dunkel_sales))

        # Recommends next beer to produce based on predicted demand.
        self.production_advice(predicted_red_helles_sales,
                               predicted_pilsner_sales, predicted_dunkel_sales)

    def production_advice(self, predicted_red_helles_sales: int,
                          predicted_pilsner_sales: int,
                          predicted_dunkel_sales: int):
        """Recommends next beer to produce based on predicted demand.

        Args:
            predicted_red_helles_sales (int): Predicted sales of Red Helles for
                                              the given month.
            predicted_pilsner_sales (int): Predicted sales of Pilsner for the
                                           given month.
            predicted_dunkel_sales (int): Predicted sales of Dunkel for the
                                          given month."""
        pass


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


class ProcessMonitoringDialog(QDialog, Ui_dialog_monitoring):
    """Contains the dialog window for process monitoring."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts volume input to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_brew_volume.setValidator(self.only_int)
        self.line_edit_ferment_volume.setValidator(self.only_int)
        self.line_edit_condition_volume.setValidator(self.only_int)
        self.line_edit_bottle_volume.setValidator(self.only_int)

        # Reads the JSON file for the list showing tank availability.
        tank_list = self.read_tanks()
        # Reads the JSON file for the list of ongoing processes.
        process_list = self.read_processes()

        # Connects the 'Refresh Processes' button to refresh processes.
        self.btn_refresh_processes.clicked.connect(
            lambda: self.refresh_processes(tank_list, process_list))
        # Connects the 'Start Hot Brew' button to start hot brew.
        self.btn_start_hot_brew.clicked.connect(
            lambda: self.start_hot_brew(process_list))
        # Connects the 'Start Fermentation' button to start fermentation.
        self.btn_start_fermentation.clicked.connect(
            lambda: self.start_fermentation(tank_list, process_list))
        # Connects the 'Start Conditioning' button to start conditioning.
        self.btn_start_conditioning.clicked.connect(
            lambda: self.start_conditioning(tank_list, process_list))
        # Connects the 'Start Bottling' button to start bottling.
        self.btn_start_bottling.clicked.connect(
            lambda: self.start_bottling(tank_list, process_list))
        # Connects the 'Abort Process' button to abort process.
        self.btn_abort_process.clicked.connect(
            lambda: self.abort_process(tank_list, process_list))

        # Updates the tank availability displayed in the UI.
        self.update_tanks()
        # Updates the process list in the UI.
        self.update_processes()

    def read_processes(self) -> list:
        """Reads the JSON file for the list of ongoing processes.

        Returns:
            process_list (list): A list of ongoing processes.
        """
        with open("ongoing_processes.json", "r") as process_file:
            try:
                process_list = json.load(process_file)
            except ValueError:
                print("Empty JSON file.")

        return process_list

    def read_tanks(self) -> list:
        """Reads the JSON file for the list showing tank availability.

        Returns:
            tank_list (list): A list showing tank availability.
        """
        with open("tanks.json", "r") as tanks_file:
            try:
                tank_list = json.load(tanks_file)
            except ValueError:
                print("Empty JSON file.")

        return tank_list

    def remove_used_processes(self, process_list: list):
        """Removes process from process list if they've been used up.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        for existing_process in process_list:
            if existing_process["volume"] == 0:
                process_list.remove(existing_process)

    def update_tanks(self):
        """Updates the tank availability displayed in the UI."""
        display_tanks = ""

        tank_list = self.read_tanks()

        # Iterates through tanks and adds their details to a tank list.
        for tank in tank_list:
            display_tanks += (tank["tank"] + ": " +
                              str(tank["volume"]) +
                              " L (" + tank["capability"] + ")\n")

        # Displays list of tank availability in UI.
        self.lbl_tanks.setText(display_tanks.rstrip())

    def update_processes(self):
        """Updates the process list in the UI."""
        display_processes = ""

        process_list = self.read_processes()

        # Iterates through processes and adds their details to a process list.
        for process in process_list:
            display_processes += (process["process"] + ", " + process["recipe"]
                                  + ", " + process["tank"] + ", " +
                                  str(process["volume"]) +
                                  " L (Completion Time: "
                                  + process["completion"] + ")\n")

        # Displays list of process details in UI.
        self.lbl_processes.setText(display_processes.rstrip())

    def refresh_processes(self, tank_list: list, process_list: list):
        """Removes finished bottling from process list and adds to inventory.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        (inventory_list, red_helles_volume, pilsner_volume,
         dunkel_volume) = InventoryManagementDialog.read_inventory(self)

        for existing_process in process_list:
            if (existing_process["process"] == "Bottling" and
                datetime.strptime(existing_process["completion"],
                                  "%d/%m/%Y %H:%M:%S")
                    <= datetime.now()):
                # Adds the bottled volume of relevant beer to the inventory.
                for inventory in inventory_list:
                    if (existing_process["recipe"] == "Organic Red Helles" and
                            inventory["recipe"] == "red_helles"):
                        inventory["volume"] += (existing_process["volume"])
                    elif (existing_process["recipe"] == "Organic Pilsner" and
                          inventory["recipe"] == "pilsner"):
                        inventory["volume"] += (existing_process["volume"])
                    elif (existing_process["recipe"] == "Organic Dunkel" and
                          inventory["recipe"] == "pilsner"):
                        inventory["volume"] += (existing_process["volume"])
                # Removes finished bottling process from process list.
                process_list.remove(existing_process)

        # Saves the newly updated inventory.
        InventoryManagementDialog.save_inventory(self, inventory_list)
        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the process list in the UI.
        self.update_processes()

    def save_tanks(self, tank_list: list):
        """Saves the updated tank list to the JSON file.

        Args:
            tank_list (list): A list of ongoing processes.
        """
        with open("tanks.json", "w") as tanks_file:
            json.dump(tank_list, tanks_file, ensure_ascii=False, indent=4)

    def save_processes(self, process_list: list):
        """Saves the updated process list to the JSON file.

        Args:
            process_list (list): A list of ongoing processes.
        """
        with open("ongoing_processes.json", "w") as process_file:
            json.dump(process_list, process_file, ensure_ascii=False, indent=4)

    def start_hot_brew(self, process_list: list):
        """Starts a hot brew for the given recipe and volume.

        Args:
            process_list (list): A list of ongoing processes.
        """
        # Gets the inputs for the new process.
        new_recipe = self.combo_box_brew_recipe.currentText()
        new_volume = int(self.line_edit_brew_volume.text())

        # Sets the completion date to three hours later.
        epoch_time = time() + 10800
        completion_date = strftime("%d/%m/%Y %H:%M:%S", localtime(epoch_time))

        # Creates the process dictionary.
        process = {"process": "Hot Brew",
                   "recipe": new_recipe,
                   "tank": "N/A",
                   "volume": new_volume,
                   "completion": completion_date}

        # Appends the process to the process list.
        process_list.append(dict(process))

        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the process list in the UI.
        self.update_processes()

    def start_fermentation(self, tank_list: list, process_list: list):
        """Starts fermentation for the given recipe, tank, and volume.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        # Gets the inputs for the new process.
        new_recipe = self.combo_box_ferment_recipe.currentText()
        new_tank = self.combo_box_ferment_tank.currentText()
        new_volume = int(self.line_edit_ferment_volume.text())

        # Sets the completion date to four weeks later.
        epoch_time = time() + 2419200
        completion_date = strftime("%d/%m/%Y %H:%M:%S", localtime(epoch_time))

        # Creates the process dictionary.
        process = {"process": "Fermentation",
                   "recipe": new_recipe,
                   "tank": new_tank,
                   "volume": new_volume,
                   "completion": completion_date}

        # Calculates the available volume from the selected tank.
        for tank in tank_list:
            if new_tank == tank["tank"]:
                allowed_volume = int(tank["volume"])

        # Checks if prerequisite process has been completed.
        for existing_process in process_list:
            if (existing_process["process"] == "Hot Brew" and
                existing_process["recipe"] == new_recipe and
                existing_process["volume"] >= new_volume and
                datetime.strptime(
                    existing_process["completion"], "%d/%m/%Y %H:%M:%S")
                    <= datetime.now()
                    and new_volume <= allowed_volume):
                # Adds process details to the list.
                process_list.append(dict(process))

                for tank in tank_list:
                    # Removes volume from tank being used for process.
                    if tank["tank"] == new_tank:
                        tank["volume"] -= new_volume

                # Removes volume from the prerequisite process.
                existing_process["volume"] -= new_volume
                break

        # Removes process from process list if they've been used up.
        self.remove_used_processes(process_list)
        # Saves the updated tank list to the JSON file.
        self.save_tanks(tank_list)
        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the tank availability displayed in the UI.
        self.update_tanks()
        # Updates the process list in the UI.
        self.update_processes()

    def start_conditioning(self, tank_list: list, process_list: list):
        """Starts conditioning for the given recipe, tank, and volume.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        # Gets the inputs for the new process.
        new_recipe = self.combo_box_condition_recipe.currentText()
        new_tank = self.combo_box_condition_tank.currentText()
        new_volume = int(self.line_edit_condition_volume.text())

        # Sets the completion date to two weeks later.
        epoch_time = time() + 1209600
        completion_date = strftime("%d/%m/%Y %H:%M:%S", localtime(epoch_time))

        # Creates the process dictionary.
        process = {"process": "Conditioning",
                   "recipe": new_recipe,
                   "tank": new_tank,
                   "volume": new_volume,
                   "completion": completion_date}

        # Calculates the available volume from the selected tank.
        for tank in tank_list:
            if new_tank == tank["tank"]:
                allowed_volume = int(tank["volume"])

        # Checks if prerequisite process has been completed.
        for existing_process in process_list:
            if (existing_process["process"] == "Fermentation" and
                existing_process["recipe"] == new_recipe and
                existing_process["volume"] >= new_volume and
                datetime.strptime(
                    existing_process["completion"], "%d/%m/%Y %H:%M:%S")
                    <= datetime.now()
                    and new_volume <= allowed_volume):
                # Adds process details to the list.
                process_list.append(dict(process))

                for tank in tank_list:
                    # Removes volume from tank being used for process.
                    if tank["tank"] == new_tank:
                        tank["volume"] -= new_volume
                    # Adds volume to tank of prerequisite.
                    if tank["tank"] == existing_process["tank"]:
                        tank["volume"] += new_volume

                # Removes volume from the prerequisite process.
                existing_process["volume"] -= new_volume
                break

        # Removes process from process list if they've been used up.
        self.remove_used_processes(process_list)
        # Saves the updated tank list to the JSON file.
        self.save_tanks(tank_list)
        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the tank availability displayed in the UI.
        self.update_tanks()
        # Updates the process list in the UI.
        self.update_processes()

    def start_bottling(self, tank_list: list, process_list: list):
        """Starts bottling for the given recipe and volume.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        # Gets the inputs for the new process.
        new_recipe = self.combo_box_bottle_recipe.currentText()
        new_volume = int(self.line_edit_bottle_volume.text())

        # Sets the completion date to 10 minutes per bottle later.
        epoch_time = time() + ((new_volume / 0.5) * 600)
        completion_date = strftime("%d/%m/%Y %H:%M:%S", localtime(epoch_time))

        # Creates the process dictionary.
        process = {"process": "Bottling",
                   "recipe": new_recipe,
                   "tank": "N/A",
                   "volume": new_volume,
                   "completion": completion_date}

        # Checks if prerequisite process has been completed.
        for existing_process in process_list:
            if (existing_process["process"] == "Conditioning" and
                existing_process["recipe"] == new_recipe and
                existing_process["volume"] >= new_volume and
                datetime.strptime(
                    existing_process["completion"], "%d/%m/%Y %H:%M:%S")
                    <= datetime.now()):
                # Adds process details to the list.
                process_list.append(dict(process))

                for tank in tank_list:
                    # Adds volume to tank of prerequisite.
                    if tank["tank"] == existing_process["tank"]:
                        tank["volume"] += new_volume

                # Removes volume from the prerequisite process.
                existing_process["volume"] -= new_volume
                break

        # Removes process from process list if they've been used up.
        self.remove_used_processes(process_list)
        # Saves the updated tank list to the JSON file.
        self.save_tanks(tank_list)
        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the tank availability displayed in the UI.
        self.update_tanks()
        # Updates the process list in the UI.
        self.update_processes()

    def abort_process(self, tank_list: list, process_list: list):
        """Aborts the given process and removes it from the process list.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        # Gets the inputs for the process to abort.
        abort_process = self.combo_box_abort_process.currentText()
        abort_recipe = self.combo_box_abort_recipe.currentText()
        abort_tank = self.combo_box_abort_tank.currentText()
        abort_volume = int(self.line_edit_abort_volume.text())
        abort_completion = self.date_time_edit_completion.text()

        # Checks for selected process in the process list.
        for existing_process in process_list:
            if (abort_process == existing_process["process"] and
                abort_recipe == existing_process["recipe"] and
                abort_tank == existing_process["tank"] and
                abort_volume == existing_process["volume"] and
                    abort_completion == existing_process["completion"]):
                for tank in tank_list:
                    # Adds volume to tank of removed process.
                    if tank["tank"] == existing_process["tank"]:
                        tank["volume"] += abort_volume

                # Removes selected process to abort.
                process_list.remove(existing_process)

        # Saves the updated tank list to the JSON file.
        self.save_tanks(tank_list)
        # Saves the updated process list to the JSON file.
        self.save_processes(process_list)
        # Updates the tank availability displayed in the UI.
        self.update_tanks()
        # Updates the process list in the UI.
        self.update_processes()


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
