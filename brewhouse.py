"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""

import csv
import pandas


def main():
    read_sales_data()


def read_sales_data():
    """
    Reads the sales data and loads it, then interprets the data.

    Returns:

    """
    with open("sales_data.csv") as file:
        file.next()
        total_sales = sum(int(row[7]) for row in csv.reader(file))

    """data_frame = pandas.read_csv("sales_data.csv")
    print(data_frame)"""


def get_avg_growth_rate():
    """
    Calculates the average growth rate from sales data.

    Returns:
        avg_growth_rate (float):
    """
    pass


def get_sales_ratio():
    """
    Calculates the ratio of sales for different beers from sales data.

    Returns:
        sales_ratio (float):
    """
    pass


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    main()
