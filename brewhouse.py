"""
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse.
"""


def main():
    read_sales_data()


def read_sales_data():
    """
    Reads the sales data and loads it, then interprets the data.

    Returns:
 
    """
    with open("sales_data.csv", "r") as file:
        pass


# Prevents the code from executing when the script is imported as a module.
if __name__ == "__main__":
    app.run(debug=True)
