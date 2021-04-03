# brewhouse-management

A system to predict demand and help monitor and schedule brewing processes for
a brewhouse.

## Visuals
![Sales Predictions](https://i.imgur.com/3S2AThA.gif)
![Inventory Management](https://i.imgur.com/zpZNONO.gif)


## Installation

These instructions will help you to get the software for Barnaby's Brewhouse
running on your computer.

### Python Version

Python 3.7.0 or later is required for this software to run. It can be installed
from [Python's website here.](https://www.python.org/getit/)

### Python Modules

The following Python modules must be installed, as they are not built into the
Python installation by default:

- pandas [for CSV handling]

```
pip install pandas
```

- pyqt5 [for user interfaces]

```
pip install pyqt5
```

## Usage

### Main Window and Sales Predictions

Start running the software by opening `brewhouse.py` in your integrated
developer environment (IDE) of choice, such as PyCharm, Visual Studio Code, or
IDLE, and running the Python file from there. Alternatively, you could navigate
to the file directory where the files have been saved in your operating
system's terminal using the `cd [DIRECTORY]` command (`cd` followed by the file
directory), and run `brewhouse.py` by entering the command
`python brewhouse.py`.

This will open the main window for the software. You will be presented with the
total sales, sales ratios, and average monthly growth percentages from the
existing sales data. You can predict sales by entering a month, and the
software will display an estimate of the volume of each beer which will be
ordered that month based on the average monthly growth in sales for each beer.
It will also give advice on which beer should be produced next, based on which
beer has the largest volume deficit, and this advice can be useful when
managing the production process in the `Process Monitoring` section of the
software.

At the top, you can navigate to other sections of the software; there are
buttons to navigate to inventory management and process monitoring.

### Inventory Management

The `Inventory Management` button will open a dialog which displays the current
inventory of each beer in Barnaby's Brewhouse in terms of both volume and
number of 500 ml bottles. You can also add or remove volume of a given beer by
selecting the beer recipe and volume, then clicking on a button to
`Add to Inventory` or `Remove from Inventory`. A negative volume is
purposefully allowed so debts of volumes can be accounted for. Inventory data
is automatically saved whenever changes are made.

Customer orders can be added in from the `Inventory Management` section as
well. The user can add an order ID, beer, and volume to record the customer
order. Once they've dispatched the order, they can record the dispatch by
entering the order ID, which will remove the volume of the appropriate beer
from the inventory of the brewhouse.

### Process Monitoring

The `Process Monitoring` button will open a dialog which displays the
availability of tanks for fermentation and conditioning, and ongoing brewing
processes. You can start different brewing processes as long as any
prerequisite processes have been completed for the appropriate beer and volume
at the time. Starting a hot brew does not have any prerequisites, but
fermentation has the prerequisite of a completed hot brew, conditioning has the
prerequisite of completed fermentation, and bottling has the prerequisite of
completed conditioning.

Once a valid process has been entered and started, it will be shown in the list
of ongoing processes, where you can see the type of process, beer recipe it is
being performed on, the tank being used (if applicable), volume, and completion
time. The ongoing process list is always up to date, and it will react to the
processes being started or aborted. This can be useful for checking whether you
will be able to start the next process, as you can see whether the prerequisite
process has been completed.

Processes can be aborted by entering the exact details of the process you would
like to abort. Aborting a process cannot be undone, so all details of that
process must be entered, as this will reduce cases of accidental process
abortions.

When the bottling has been completed, it means that the full beer brewing
process has been completed. You can send completed bottles to the inventory by
clicking on the `Send Bottles to Inventory` button in the `Ongoing Processes`
section. This will remove the completed bottling process, and add the volume of
beer to the inventory, which can be seen in the `Inventory Management` section
of the software.

All changes which are made in the `Process Monitoring` section are
automatically saved, so data is not lost when the window or program is closed.

### Upload Sales Data

The `Upload Sales Data` button will open a small dialog which provides a form
for the user to input the details of their new sale. Once they click the
`Upload New Sale` button, the form will be checked. If all the fields have
been filled in, the new sale will be added to the CSV file.

## Other Details

### Code Style

This project was developed using Python's
[PEP 8 style guide for code](https://www.python.org/dev/peps/pep-0008/), as it
is a commonly used standard within the Python community.

### Tools Used

[Qt Creator](https://www.qt.io/download) was used to design the user interfaces
for this project in a what you see is what you get (WYSIWYG) editor.

PyQt5's
[pyuic5](https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html)
was used to generate the base Python code from the user interface designs,
effectively converting the `.ui` files to `.py` files. I edited the generated
code to conform to PEP 8 guidelines, and added documentation to make the code
easier to understand. These generated code files were marked with the
`_setup.py` suffixes, such as `brewhouse_setup.py`, and they were imported into
the other Python files such as `brewhouse.py` so that functionality could be
developed for the user interface objects.

## GitHub Repository

The Git repository for this software project can be found on
[GitHub here.](https://github.com/IsaacCheng9/brewhouse) In this repository,
you can view the version history of files for this project, meaning you can see
the version history with changelogs and how development occurred over time. You
can also flag issues with the software from this repository.