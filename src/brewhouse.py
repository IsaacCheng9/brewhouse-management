"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse. The user is presented with the statistics on total sales,
sales ratios, and average monthly growth rates calculated from the existing
sales data. They can select a date and receive a sales prediction for the month
of that date for each beer being sold. The user can also navigate to the
inventory management, process monitoring, and upload new sales sections, which
will allow them to manage the company's inventory, manage the production
stages of different beers, and upload new sales data respectively.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Tuple

import pandas
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow

from inv_management import InventoryManagementDialog
from process_monitoring import ProcessMonitoringDialog
from setup.brewhouse_setup import Ui_mwindow_brewhouse
from upload_sales import UploadSalesDialog


def main() -> None:
    """Opens the program window, and exits program when window is closed."""
    # Performs scaling to prevent tiny UI on high resolution screens.
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
    os.environ["QT_SCALE_FACTOR"] = "1.5"
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("fusion")
    setup_logging()
    mwindow_brewhouse = BrewhouseWindow()
    mwindow_brewhouse.show()
    sys.exit(app.exec())


def setup_logging():
    """
    Sets up the logging system to automatically log actions to log file.
    """
    # No restoration from logging; data is always persisted in files anyway.
    logging.basicConfig(
        filename="resources/logs.txt",
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    logging.debug("Barnaby's Brewhouse program started.")


def read_sales_data() -> pandas.core.frame.DataFrame:
    """Reads the sales data and loads it to a variable.

    Returns:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.
    """
    data_frame = pandas.read_csv("resources/sales_data.csv")
    print(str(data_frame) + "\n")

    return data_frame


class BrewhouseWindow(QMainWindow, Ui_mwindow_brewhouse):
    """Contains the main window for the Brewhouse application."""

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)

        # Connects 'Inventory Management' button to the inventory dialog.
        self.btn_inv_management.clicked.connect(self.open_dialog_inv_management)
        # Connects 'Process Monitoring' button to the monitoring dialog.
        self.btn_process_monitoring.clicked.connect(self.open_dialog_monitoring)
        # Connects 'Upload Sales Data' button to the upload sales dialog.
        self.btn_upload_sales.clicked.connect(self.open_dialog_upload_sales)

        # Reads sales data from the CSV file.
        data_frame = read_sales_data()
        # Calculates total sales and sales ratios of beer.
        self.get_sales_ratio(data_frame)
        # Calculates average monthly growth rates in sales of beer.
        (
            beers,
            red_helles_growth,
            pilsner_growth,
            dunkel_growth,
        ) = self.get_avg_growth_rate(data_frame)

        # Predicts future sales of a given beer in a given month.
        self.btn_predict.clicked.connect(
            lambda: self.predict_sales(
                data_frame, red_helles_growth, pilsner_growth, dunkel_growth
            )
        )

    def open_dialog_inv_management(self) -> None:
        """Opens the dialog for the user to manage inventory."""
        self.Dialog = InventoryManagementDialog()
        self.Dialog.open()

    def open_dialog_monitoring(self) -> None:
        """Opens the dialog for the user to monitor brewing processes."""
        self.Dialog = ProcessMonitoringDialog()
        self.Dialog.open()

    def open_dialog_upload_sales(self) -> None:
        """Opens the dialog for the user to upload new sales data."""
        self.Dialog = UploadSalesDialog()
        self.Dialog.open()

    def get_sales_ratio(self, data_frame: pandas.core.frame.DataFrame):
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
        self.lbl_overall_sales.setText("Overall: " + str(total_sales))
        self.lbl_red_helles_sales.setText(
            "Organic Red Helles: " + str(red_helles_sales)
        )
        self.lbl_pilsner_sales.setText("Organic Pilsner: " + str(pilsner_sales))
        self.lbl_dunkel_sales.setText("Organic Dunkel: " + str(dunkel_sales))
        self.lbl_red_helles_ratio.setText(
            "Organic Red Helles: " + str(red_helles_ratio) + "%"
        )
        self.lbl_pilsner_ratio.setText("Organic Pilsner: " + str(pilsner_ratio) + "%")
        self.lbl_dunkel_ratio.setText("Organic Dunkel: " + str(dunkel_ratio) + "%")

    def get_avg_growth_rate(
        self, data_frame: pandas.core.frame.DataFrame
    ) -> Tuple[list, float, float, float]:
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
        months = [
            "Nov-18",
            "Dec-18",
            "Jan-19",
            "Feb-19",
            "Mar-19",
            "Apr-19",
            "May-19",
            "Jun-19",
            "Jul-19",
            "Aug-19",
            "Sep-19",
            "Oct-19",
        ]
        beers = ["Organic Red Helles", "Organic Pilsner", "Organic Dunkel"]

        # Iterates through monthly sales of each type of beer.
        for beer in beers:
            month_filter_previous = data_frame["Date Required"].str.contains("Nov-18")
            for month in months:
                month_filter_current = data_frame["Date Required"].str.contains(month)
                beer_filter = data_frame["Recipe"].isin([beer])

                # Filters data to the sales in a month for that type of beer.
                month_data_current = data_frame[month_filter_current & beer_filter]
                month_data_previous = data_frame[month_filter_previous & beer_filter]
                month_sales_current = int(month_data_current["Quantity ordered"].sum())
                month_sales_previous = int(
                    month_data_previous["Quantity ordered"].sum()
                )

                # Accumulates growth rate for each type of beer.
                if beer == "Organic Red Helles" and month != "Nov-18":
                    red_helles_growth += month_sales_current / month_sales_previous
                elif beer == "Organic Pilsner" and month != "Nov-18":
                    pilsner_growth += month_sales_current / month_sales_previous
                elif beer == "Organic Dunkel" and month != "Nov-18":
                    dunkel_growth += month_sales_current / month_sales_previous

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
            "Organic Red Helles: " + str(red_helles_growth_pct) + "%"
        )
        self.lbl_pilsner_growth.setText(
            "Organic Pilsner: " + str(pilsner_growth_pct) + "%"
        )
        self.lbl_dunkel_growth.setText(
            "Organic Dunkel: " + str(dunkel_growth_pct) + "%"
        )

        return beers, red_helles_growth, pilsner_growth, dunkel_growth

    def predict_sales(
        self,
        data_frame: pandas.core.frame.DataFrame,
        red_helles_growth: float,
        pilsner_growth: float,
        dunkel_growth: float,
    ):
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
        prediction_date = datetime.strptime(prediction_date, format_date).date()
        month_difference = (prediction_date.year - final_date.year) * 12 + (
            prediction_date.month - final_date.month
        )

        # Filters to last month's sales of Red Helles, Pilsner, and Dunkel.
        last_month_filter = data_frame["Date Required"].str.contains("Oct-19")
        red_helles_filter = data_frame["Recipe"].str.contains("Organic Red Helles")
        pilsner_filter = data_frame["Recipe"].str.contains("Organic Pilsner")
        dunkel_filter = data_frame["Recipe"].str.contains("Organic Dunkel")

        # Gets last month's sales of Red Helles, Pilsner, and Dunkel.
        last_red_helles_data = data_frame[last_month_filter & red_helles_filter]
        last_pilsner_data = data_frame[last_month_filter & pilsner_filter]
        last_dunkel_data = data_frame[last_month_filter & dunkel_filter]
        last_red_helles_sales = int(last_red_helles_data["Quantity ordered"].sum())
        last_pilsner_sales = int(last_pilsner_data["Quantity ordered"].sum())
        last_dunkel_sales = int(last_dunkel_data["Quantity ordered"].sum())

        # Predicts beer sales for given month, rounded down to nearest integer.
        predicted_red_helles_sales = int(
            (last_red_helles_sales * (red_helles_growth ** month_difference))
        )
        predicted_pilsner_sales = int(
            (last_pilsner_sales * (pilsner_growth ** month_difference))
        )
        predicted_dunkel_sales = int(
            (last_dunkel_sales * (dunkel_growth ** month_difference))
        )

        # Shows the calculations of sales predictions for the given date in UI.
        self.lbl_predictions.setText(
            "(Last Monthly Beer Sales * (Average Beer Growth Rate ^ "
            + "Month Difference))\nOrganic Red Helles: ("
            + str(last_red_helles_sales)
            + " * ("
            + str(red_helles_growth)
            + " ^ "
            + str(month_difference)
            + ")) = "
            + str(predicted_red_helles_sales)
            + " L\nOrganic Pilsner: ("
            + str(last_pilsner_sales)
            + " * ("
            + str(pilsner_growth)
            + " ^ "
            + str(month_difference)
            + ")) = "
            + str(predicted_pilsner_sales)
            + " L\nOrganic Dunkel: ("
            + str(last_dunkel_sales)
            + " * ("
            + str(dunkel_growth)
            + " ^ "
            + str(month_difference)
            + ")) = "
            + str(predicted_dunkel_sales)
            + " L"
        )

        # Recommends next beer to produce based on predicted demand.
        self.production_advice(
            predicted_red_helles_sales, predicted_pilsner_sales, predicted_dunkel_sales
        )

    def production_advice(
        self,
        predicted_red_helles_sales: int,
        predicted_pilsner_sales: int,
        predicted_dunkel_sales: int,
    ):
        """Recommends next beer to produce based on predicted demand.

        Args:
            predicted_red_helles_sales (int): Predicted sales of Red Helles for
                                              the given month.
            predicted_pilsner_sales (int): Predicted sales of Pilsner for the
                                           given month.
            predicted_dunkel_sales (int): Predicted sales of Dunkel for the
                                          given month.
        """
        red_helles_production = int()
        pilsner_production = int()
        dunkel_production = int()
        recommendation = str()

        # Reads the inventory data to access volumes of each beer.
        (
            inventory_list,
            red_helles_volume,
            pilsner_volume,
            dunkel_volume,
        ) = InventoryManagementDialog.read_inventory(self)
        # Reads the processes data to access volumes of each beer being made.
        process_list = ProcessMonitoringDialog.read_processes(self)

        # Sums the volume of each beer currently in production processes.
        for process in process_list:
            if process["recipe"] == "Organic Red Helles":
                red_helles_production = process["volume"]
            elif process["recipe"] == "Organic Pilsner":
                pilsner_production = process["volume"]
            elif process["recipe"] == "Organic Dunkel":
                dunkel_production = process["volume"]

        # Calculates the deficit in volume of each beer.
        red_helles_deficit = (
            predicted_red_helles_sales - red_helles_volume - red_helles_production
        )
        pilsner_deficit = predicted_pilsner_sales - pilsner_volume - pilsner_production
        dunkel_deficit = predicted_dunkel_sales - dunkel_volume - dunkel_production

        # Recommends producing the beer with the largest volume deficit.
        largest_deficit = max(red_helles_deficit, pilsner_deficit, dunkel_deficit)
        deficit_calculation = (
            "(Beer Deficit = Estimated Demand - Inventory "
            "Volume - Volume in Production)\n"
            "Organic Red Helles Deficit:  "
            + str(predicted_red_helles_sales)
            + " - "
            + str(red_helles_volume)
            + " - "
            + str(red_helles_production)
            + " = "
            + str(red_helles_deficit)
            + " L\nOrganic Pilsner Deficit: "
            + str(predicted_pilsner_sales)
            + " - "
            + str(pilsner_volume)
            + " - "
            + str(pilsner_production)
            + " = "
            + str(pilsner_deficit)
            + " L\nOrganic Dunkel Deficit:  "
            + str(predicted_dunkel_sales)
            + " - "
            + str(dunkel_volume)
            + " - "
            + str(dunkel_production)
            + " = "
            + str(dunkel_deficit)
            + " L\n"
        )
        if largest_deficit == red_helles_deficit:
            recommendation = (
                "\nOrganic Red Helles would be the best beer to "
                "produce next, as it has the largest deficit."
            )
        elif largest_deficit == pilsner_deficit:
            recommendation = (
                "\nOrganic Pilsner would be the best beer to "
                "produce next, as it has the largest deficit."
            )
        elif largest_deficit == dunkel_deficit:
            recommendation = (
                "\nOrganic Dunkel would be the best beer to "
                "produce next, as it has the largest deficit."
            )

        # Updates the UI with the deficit calculations and the recommendation.
        self.lbl_advice.setText(deficit_calculation + recommendation)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
