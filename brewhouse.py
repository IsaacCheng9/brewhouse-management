"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

from datetime import datetime
from typing import Tuple

import pandas


def main() -> None:
    """
    """
    data_frame = read_sales_data()
    (red_helles_ratio, pilsner_ratio,
     dunkel_ratio) = get_sales_ratio(data_frame)
    (beers, red_helles_growth, pilsner_growth,
     dunkel_growth) = get_avg_growth_rate(data_frame)
    predict_sales(data_frame, beers, red_helles_growth,
                  pilsner_growth, dunkel_growth)


def read_sales_data() -> pandas.core.frame.DataFrame:
    """
    Reads the sales data and loads it to a variable.

    Returns:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.
    """
    data_frame = pandas.read_csv("sales_data.csv")
    print(str(data_frame) + "\n")

    return data_frame


def get_sales_ratio(data_frame:
                    pandas.core.frame.DataFrame) -> Tuple[float, float, float]:
    """
    Calculates the ratio of sales for different beers from sales data.

    Args:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.

    Returns:
        red_helles_ratio (float): Sales ratio of Organic Red Helles.
        pilsner_ratio (float): Sales ratio of Organic Pilsner.
        dunkel_ratio (float): Sales ratio of Organic Dunkel.
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

    return red_helles_ratio, pilsner_ratio, dunkel_ratio


def get_avg_growth_rate(data_frame:
                        pandas.core.frame.DataFrame) -> Tuple[list, float,
                                                              float, float]:
    """
    Calculates the average monthly growth rate from sales data.

    Args:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.

    Returns:
        beers (list): A list of the beers.
        red_helles_growth (float): Average growth rate of sales for Red Helles.
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
            month_filter_current = data_frame["Date Required"].str.contains(
                month)
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
    print("\nRed Helles Growth: " + str(red_helles_growth) +
          "\nPilsner Growth: " + str(pilsner_growth) + "\nDunkel Growth: " +
          str(dunkel_growth))

    return beers, red_helles_growth, pilsner_growth, dunkel_growth


def predict_sales(data_frame:
                  pandas.core.frame.DataFrame, beers: list,
                  red_helles_growth: float, pilsner_growth: float,
                  dunkel_growth: float):
    """
    Calculates future sales of Red Helles, Pilsner, and Dunkel using previous
    sales data.

    Args:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.
        beers (list): A list of the beers.
        red_helles_growth (float): Average growth rate of sales for Red Helles.
        pilsner_growth (float): Average growth rate of sales for Pilsner.
        dunkel_growth (float): Average growth rate of sales for Dunkel.
    """
    """months = ["Nov-19", "Dec-19", "Jan-20", "Feb-20", "Mar-20", "Apr-20",
              "May-20", "Jun-20", "Jul-20", "Aug-20", "Sep-20", "Oct-20",
              "Nov-20"]

    for beer in beers:
        month_filter_previous = data_frame["Date Required"].str.contains(
            "Oct-19")
        for month in months:
            beer_filter = data_frame["Recipe"].isin([beer])"""

    # Gets the month and year to predict from the user.
    format_date = "%d/%m/%Y"
    prediction_beer = input("Please enter which beer you would like to "
                            "predict sales for: ")
    prediction_date = input("Please enter the date you would like the "
                            "prediction for (DD/MM/YYYY): ")
    prediction_date = datetime.strptime(prediction_date, format_date).date()
    # month_prediction = prediction_date[:2]
    # year_prediction = prediction_date[3:7]
    month_difference = (prediction_date.to_period("M") -
                        (2019-10-1).to_period("M"))
    print(month_difference)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
