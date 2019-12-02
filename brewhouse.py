"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

import pandas


def main():
    data_frame = read_sales_data()
    get_sales_ratio(data_frame)
    get_avg_growth_rate(data_frame)


def read_sales_data() -> pandas.core.frame.DataFrame:
    """
    Reads the sales data and loads it to a variable.

    Returns:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.
    """
    data_frame = pandas.read_csv("sales_data.csv")
    print(str(data_frame) + "\n")

    return data_frame


def get_sales_ratio(data_frame: pandas.core.frame.DataFrame) -> float:
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
    print(str(total_sales) + "\n")

    # Sums Red Helles sales and calculates their sales ratio.
    red_helles = data_frame.query("Recipe == 'Organic Red Helles'")
    red_helles_sales = int(red_helles["Quantity ordered"].sum())
    print(str(red_helles_sales))
    red_helles_ratio = round((red_helles_sales / total_sales) * 100, 3)
    print("Organic Red Helles: " + str(red_helles_ratio) + "%\n")

    # Sums Pilsner sales and calculates their sales ratio.
    pilsner = data_frame.query("Recipe == 'Organic Pilsner'")
    pilsner_sales = int(pilsner["Quantity ordered"].sum())
    print(str(pilsner_sales))
    pilsner_ratio = round((pilsner_sales / total_sales) * 100, 3)
    print("Organic Pilsner: " + str(pilsner_ratio) + "%\n")

    # Sums Dunkel sales and calculates their sales ratio.
    dunkel = data_frame.query("Recipe == 'Organic Dunkel'")
    dunkel_sales = int(dunkel["Quantity ordered"].sum())
    print(str(dunkel_sales))
    dunkel_ratio = round((dunkel_sales / total_sales) * 100, 3)
    print("Organic Dunkel: " + str(dunkel_ratio) + "%\n")

    return red_helles_ratio, red_helles_ratio, dunkel_ratio


def get_avg_growth_rate(data_frame: pandas.core.frame.DataFrame) -> float:
    """
    Calculates the average monthly growth rate from sales data.

    Args:
        data_frame (pandas.core.frame.DataFrame): Sales data of beers.

    Returns:
        red_helles_growth_rate (float):
        pilsner_growth_rate (float):
        dunkel_growth_rate (float):
    """
    """# Sets filters for each month.
    nov18_filter = data_frame["Date Required"].str.contains("Nov-18")

    # Calculates Nov-18 sales for Red Helles.
    red_helles_filter = data_frame["Recipe"].isin(["Organic Red Helles"])
    red_helles_nov18 = data_frame[nov18_filter & red_helles_filter]
    red_helles_nov18_sales = red_helles_nov18["Quantity ordered"].sum()
    print(red_helles_nov18_sales)"""

    red_helles_growth = []
    pilsner_growth = []
    dunkel_growth = []
    month_filter_previous = data_frame["Date Required"].str.contains("Nov-18")

    # Sets filters for each month.
    months = ["Nov-18", "Dec-18", "Jan-19", "Feb-19", "Mar-19", "Apr-19",
              "May-19", "Jun-19", "Jul-19", "Aug-19", "Sep-19", "Oct-19"]
    beers = ["Organic Red Helles", "Organic Pilsner", "Organic Dunkel"]
    for beer in beers:
        for month in months:
            # Calculates average monthly growth rate for each type of beer.
            month_filter_current = data_frame["Date Required"].str.contains(month)
            beer_filter = data_frame["Recipe"].isin([beer])
            if beer == "Organic Red Helles":
                red_helles_data_current = data_frame[month_filter_current & beer_filter]
                red_helles_data_previous = data_frame[month_filter_previous & beer_filter]
                red_helles_sales_current = red_helles_data_current["Quantity ordered"].sum(
                )
                red_helles_sales_previous = red_helles_data_previous["Quantity ordered"].sum(
                )
                if month != "Nov-18":
                    red_helles_growth += (red_helles_sales_current -
                                          red_helles_sales_previous)
            month_filter_previous = month_filter_current

    print(red_helles_growth)


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
