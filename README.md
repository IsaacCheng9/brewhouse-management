# Barnaby's Brewhouse
A system to predict demand and help monitor and schedule brewing processes for
Barnaby's Brewhouse. The user is presented with the statistics on total sales,
sales ratios, and average monthly growth rates calculated from the existing
sales data. They can select a date and receive a sales prediction for the month
of that date for each beer being sold. The user can also navigate to the
inventory management and process monitoring sections, which will allow them
to manage the company's inventory and manage the production stages of different
beers respectively.

## Getting Started
These instructions will help you to get the software for Barnaby's Brewhouse
running on your computer.

### Prerequisites
Python 3.7.0 or later is required for this software to run. It can be installed
from [Python's website here.](https://www.python.org/getit/)

### Installing
The following Python modules must be installed, as they are not built into
the Python installation by default:
- pandas [for CSV handling]
```
pip install pandas
```
- pyqt5 [for user interfaces]
```
pip install pyqt5
```

Ensure that all files are installed in the same folder on your computer, as
they will need to be able to access one another for full functionality. The
`.py` files are needed for all the code in the software to work, the `.json`
files are needed for data persistence to function, and the `.csv` file is
needed so that existing sales data can be accessed.

## Usage


## Other Details

### Code Style
This project was developed using [Python's PEP 8 style guide for code](https://www.python.org/dev/peps/pep-0008/), as it is a commonly used standard within the Python community.

### Tools Used
[Qt Creator](https://www.qt.io/download) was used to design the user interfaces
for this project in a what you see is what you get (WYSIWYG) editor.

[PyQt5's `pyuic5`](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html) was used to generate the base Python code from the user interface designs,
effectively converting the `.ui` files to `.py` files. I edited the generated
code to conform to PEP 8 guidelines, and added documentation to make the code
easier to understand. These generated code files were marked with the
`_setup.py` suffixes, such as `brewhouse_setup.py`, and they were imported into
the other Python files such as `brewhouse.py` so that functionality could be
developed for the user interface objects. 

### GitHub Repository
The Git repository for this software project can be found on [GitHub here.](https://github.com/IsaacCheng9/brewhouse) In this repository, you can view the version
history of files for this project, meaning you can see the version history and
how development occurred over time. You can also flag issues with the software
from this repository.