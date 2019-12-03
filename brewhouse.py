"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

import sys
from datetime import datetime
from typing import Tuple

import pandas
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QMainWindow

from brewhouse_setup import Ui_mwindow_brewhouse


def main() -> None:
    """
    """
    app = QtWidgets.QApplication(sys.argv)
    mwindow_brewhouse = BrewhouseWindow()
    mwindow_brewhouse.show()
    sys.exit(app.exec())


class BrewhouseWindow(QMainWindow, Ui_mwindow_brewhouse):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Reads sales data from the CSV file.
        data_frame = self.read_sales_data()

        # Calculates total sales and sales ratios of beer.
        (total_sales, red_helles_sales, red_helles_ratio,
         pilsner_sales, pilsner_ratio,
         dunkel_sales, dunkel_ratio) = self.get_sales_ratio(data_frame)
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

        # Calculates average monthly growth rates in sales of beer.
        (beers, red_helles_growth, pilsner_growth,
         dunkel_growth, red_helles_growth_pct,
         pilsner_growth_pct,
         dunkel_growth_pct) = self.get_avg_growth_rate(data_frame)
        self.lbl_red_helles_growth.setText(
            "Organic Red Helles - " + str(red_helles_growth_pct) + "%")
        self.lbl_pilsner_growth.setText(
            "Organic Pilsner - " + str(pilsner_growth_pct) + "%")
        self.lbl_dunkel_growth.setText(
            "Organic Dunkel - " + str(dunkel_growth_pct) + "%")

        # Predicts future sales of a given beer in a given month.
        self.btn_predict.clicked.connect(lambda: self.predict_sales(
            data_frame, beers, red_helles_growth,
            pilsner_growth, dunkel_growth))

    def read_sales_data(self) -> pandas.core.frame.DataFrame:
        """
        Reads the sales data and loads it to a variable.

        Returns:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.
        """
        data_frame = pandas.read_csv("sales_data.csv")
        print(str(data_frame) + "\n")

        return data_frame

    def get_sales_ratio(self, data_frame:
                        pandas.core.frame.DataFrame) -> Tuple[int, int, float,
                                                              int, float, int,
                                                              float]:
        """
        Calculates the total sales and ratio of sales for different beers
        from sales data.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.

        Returns:
            total_sales (int): Total sales of all beers.
            red_helles_sales (int): Total sales of Red Helles.
            red_helles_ratio (float): Sales ratio of Red Helles.
            pilsner_sales (int): Total sales of Pilsner.
            pilsner_ratio (float): Sales ratio of Pilsner.
            dunkel_sales (int): Total sales of Dunkel.
            dunkel_ratio (float): Sales ratio of Dunkel.
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

        print("Total Sales: " + str(total_sales) + "\nRed Helles: " +
              str(red_helles_ratio) + "%\nPilsner: " + str(pilsner_ratio) +
              "%\nDunkel: " + str(dunkel_ratio) + "%")

        return (total_sales, red_helles_sales, red_helles_ratio, pilsner_sales,
                pilsner_ratio, dunkel_sales, dunkel_ratio)

    def get_avg_growth_rate(self, data_frame:
                            pandas.core.frame.DataFrame) -> Tuple[list, float,
                                                                  float,
                                                                  float,
                                                                  float,
                                                                  float,
                                                                  float]:
        """
        Calculates the average monthly growth rate from sales data.

        Args:
            data_frame (pandas.core.frame.DataFrame): Sales data of beers.

        Returns:
            beers (list): A list of the beers.
            red_helles_growth (float): Average growth rate of sales for Red
                                       Helles.
            pilsner_growth (float): Average growth rate of sales for Pilsner.
            dunkel_growth (float): Average growth rate of sales for Dunkel.
            red_helles_growth_pct (float): Average growth rate of sales for Red
                                           Helles shown as a percentage to 3dp.
            pilsner_growth_pct (float): Average growth rate of sales for
                                        Pilsner shown as a percentage to 3dp.
            dunkel_growth_pct (float): Average growth rate of sales for Dunkel
                                       shown as a percentage to 3dp.
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

        return (beers, red_helles_growth, pilsner_growth, dunkel_growth,
                red_helles_growth_pct, pilsner_growth_pct, dunkel_growth_pct)

    def predict_sales(self, data_frame:
                      pandas.core.frame.DataFrame, beers: list,
                      red_helles_growth: float, pilsner_growth: float,
                      dunkel_growth: float) -> int:
        """
        Calculates future sales of Red Helles, Pilsner, and Dunkel using
        previous sales data.

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

        # Predicts beer sales for that month, rouned down to nearest integer.
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
        print("\nPredicted Sales: " + str(prediction_sales))

        self.lbl_predict_result.setText(
            "Estimated Number of Sales: " + str(prediction_sales))

        return prediction_sales

        """months = ["Nov-19", "Dec-19", "Jan-20", "Feb-20", "Mar-20",
                "Apr-20", "May-20", "Jun-20", "Jul-20", "Aug-20", "Sep-20",
                "Oct-20", "Nov-20"]

        for beer in beers:
            month_filter_previous = data_frame["Date Required"].str.contains(
                "Oct-19")
            for month in months:
                beer_filter = data_frame["Recipe"].isin([beer])"""

    def process_monitoring(self):
        pass


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
