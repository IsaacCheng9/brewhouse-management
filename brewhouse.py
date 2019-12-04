"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

import json
import sys
from datetime import datetime
from typing import Tuple

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog, QMainWindow

from brewhouse_setup import Ui_mwindow_brewhouse
from inv_management_setup import Ui_dialog_inv_management
from process_monitoring_setup import Ui_dialog_monitoring


def main() -> None:
    """Opens the program window, and exits program when window is closed."""
    app = QtWidgets.QApplication(sys.argv)
    mwindow_brewhouse = BrewhouseWindow()
    mwindow_brewhouse.show()
    sys.exit(app.exec())


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
            data_frame, beers, red_helles_growth,
            pilsner_growth, dunkel_growth))

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

        print("Total Sales: " + str(total_sales) + "\nRed Helles Ratio: " +
              str(red_helles_ratio) + "%\nPilsner Ratio: " + str(pilsner_ratio) +
              "%\nDunkel Ratio: " + str(dunkel_ratio) + "%")

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
        print("\nRed Helles Growth: " + str(red_helles_growth_pct) +
              "%\nPilsner Growth: " + str(pilsner_growth_pct) +
              "%\nDunkel Growth: " + str(dunkel_growth_pct) + "%")

        # Displays percentage of sales provided by each beer.
        self.lbl_red_helles_growth.setText(
            "Organic Red Helles - " + str(red_helles_growth_pct) + "%")
        self.lbl_pilsner_growth.setText(
            "Organic Pilsner - " + str(pilsner_growth_pct) + "%")
        self.lbl_dunkel_growth.setText(
            "Organic Dunkel - " + str(dunkel_growth_pct) + "%")

        return beers, red_helles_growth, pilsner_growth, dunkel_growth

    def predict_sales(self, data_frame:
                      pandas.core.frame.DataFrame, beers: list,
                      red_helles_growth: float, pilsner_growth: float,
                      dunkel_growth: float) -> int:
        """Predicts future sales of Red Helles, Pilsner, and Dunkel.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.
            beers (list): A list of the beers.
            red_helles_growth (float): Average growth rate of sales for Red
                                       Helles.
            pilsner_growth (float): Average growth rate of sales for Pilsner.
            dunkel_growth (float): Average growth rate of sales for Dunkel.

        Returns:
            prediction-sales (int): Predicted monthly sales of a given beer for
                                    a given month.
        """

        # Gets the beer and month to predict the sales for.
        prediction_beer = self.combo_box_beer.currentText()
        prediction_date = self.date_edit_predict.text()

        # Calculates number of months since the last month of sales data.
        format_date = "%d/%m/%Y"
        final_date = datetime.strptime("30/10/2019", format_date).date()
        prediction_date = datetime.strptime(
            prediction_date, format_date).date()
        month_difference = ((prediction_date.year - final_date.year) *
                            12 + (prediction_date.month - final_date.month))

        # Predicts beer sales for that month, rounded down to nearest integer.
        last_month_filter = data_frame["Date Required"].str.contains("Oct-19")
        beer_filter = data_frame["Recipe"].str.contains(prediction_beer)
        last_month_data = data_frame[last_month_filter & beer_filter]
        last_month_sales = int(last_month_data["Quantity ordered"].sum())

        if prediction_beer == "Organic Red Helles":
            prediction_sales = int((last_month_sales *
                                    (red_helles_growth ** month_difference)))
        elif prediction_beer == "Organic Pilsner":
            prediction_sales = int((last_month_sales *
                                    (pilsner_growth ** month_difference)))
        elif prediction_beer == "Organic Dunkel":
            prediction_sales = int((last_month_sales *
                                    (dunkel_growth ** month_difference)))
        print("\nEstimated Number of Monthly Sales: " + str(prediction_sales))

        # Shows the sales prediction for the given beer and date.
        self.lbl_predict_result.setText(
            "Estimated Number of Monthly Sales: " + str(prediction_sales))


class InventoryManagementDialog(QDialog, Ui_dialog_inv_management):
    """Contains the dialog window for inventory management."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts volume input to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_update_inv_volume.setValidator(self.only_int)

        # Reads the inventory and gets volume for each beer.
        (inventory_dict, red_helles_volume, pilsner_volume,
         dunkel_volume) = self.read_inventory()

        # Connects 'Add to Inventory' button to add inventory volume.
        self.btn_add_inv.clicked.connect(lambda: self.add_inventory(
            inventory_dict, red_helles_volume, pilsner_volume, dunkel_volume))
        # Connects 'Remove from Inventory' button to remove inventory volume.
        self.btn_remove_inv.clicked.connect(lambda: self.remove_inventory(
            inventory_dict, red_helles_volume, pilsner_volume, dunkel_volume))

        # Updates the volumes in the inventory in the UI.
        self.update_inventory()

    def read_inventory(self) -> Tuple[dict, int, int, int]:
        """Reads the inventory and gets volume for each beer.

        Returns:
            inventory_dict (dict): Dictionary storing the volume for each beer.
            red_helles_volume (int): Volume (L) of Red Helles.
            pilsner_volume (int): Volume (L) of Pilsner.
            dunkel_volume (int): Volume (L) of Dunkel.
        """
        with open("inventory.json", "r") as inventory_file:
            try:
                inventory_dict = json.load(inventory_file)
                red_helles_volume = int(
                    inventory_dict["Organic Red Helles"]["Volume"])
                pilsner_volume = int(
                    inventory_dict["Organic Pilsner"]["Volume"])
                dunkel_volume = int(inventory_dict["Organic Dunkel"]["Volume"])
            except ValueError:
                print("Empty JSON file.")

        return inventory_dict, red_helles_volume, pilsner_volume, dunkel_volume

    def update_inventory(self):
        """Updates the volumes in the inventory in the UI."""
        (inventory_dict, red_helles_volume, pilsner_volume,
         dunkel_volume) = self.read_inventory()

        # Shows the volume and number of bottles of Red Helles.
        red_helles_quantity = int(red_helles_volume / 500)
        self.lbl_red_helles_inv.setText(
            "Organic Red Helles - " + str(red_helles_volume) + " L / " +
            str(red_helles_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Pilsner.
        pilsner_quantity = int(pilsner_volume / 500)
        self.lbl_pilsner_inv.setText(
            "Organic Pilsner - " + str(pilsner_volume) + " L / " +
            str(pilsner_quantity) + " bottle(s)")

        # Shows the volume and number of bottles of Dunkel.
        dunkel_quantity = int(dunkel_volume / 500)
        self.lbl_dunkel_inv.setText(
            "Organic Dunkel - " + str(dunkel_volume) + " L / " +
            str(dunkel_quantity) + " bottle(s)")

    def save_inventory(self, inventory_dict: dict):
        """Saves the new inventory to the JSON file.

        Args:
            inventory_dict (dict): Dictionary storing the volume for each beer.
        """
        with open("inventory.json", "w") as outfile:
            json.dump(inventory_dict, outfile, ensure_ascii=False, indent=4)

    def add_inventory(self, inventory_dict: dict, red_helles_volume: int,
                      pilsner_volume: int, dunkel_volume: int):
        """Adds the given volume to the given beer in the inventory.

        Args:
            inventory_dict (dict): Dictionary storing the volume for each beer.
            red_helles_volume (int): Volume (L) of Red Helles.
            pilsner_volume (int): Volume (L) of Pilsner.
            dunkel_volume (int): Volume (L) of Dunkel.
        """
        # Adds inputted volume to the selected beer.
        add_beer = self.combo_box_update_inv_recipe.currentText()
        add_volume = self.line_edit_update_inv_volume.text()
        inventory_dict[add_beer]["Volume"] += int(add_volume)

        # Saves the new inventory to the JSON file.
        self.save_inventory(inventory_dict)
        # Updates the volumes in the inventory in the UI.
        self.update_inventory()

    def remove_inventory(self, inventory_dict: dict, red_helles_volume: int,
                         pilsner_volume: int, dunkel_volume: int):
        """Removes the given volume to the given beer in the inventory.

        Args:
            inventory_dict (dict): Dictionary storing the volume for each beer.
            red_helles_volume (int): Volume (L) of Red Helles.
            pilsner_volume (int): Volume (L) of Pilsner.
            dunkel_volume (int): Volume (L) of Dunkel.
        """
        # Adds inputted volume to the selected beer.
        remove_beer = self.combo_box_update_inv_recipe.currentText()
        remove_volume = self.line_edit_update_inv_volume.text()
        inventory_dict[remove_beer]["Volume"] -= int(remove_volume)

        # Saves the new inventory to the JSON file.
        self.save_inventory(inventory_dict)
        # Updates the volumes in the inventory in the UI.
        self.update_inventory()


class ProcessMonitoringDialog(QDialog, Ui_dialog_monitoring):
    """Contains the dialog window for process monitoring."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts volume input to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_new_volume.setValidator(self.only_int)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
