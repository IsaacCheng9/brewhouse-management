"""
A system to monitor the brewing processes in Barnaby's Brewhouse, allowing the
user to view availability tanks, view ongoing processes, start new processes,
and abort existing processes.
"""

import json
from datetime import datetime
from time import localtime, strftime, time

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from inv_management import InventoryManagementDialog
from setup.process_monitoring_setup import Ui_dialog_monitoring


def remove_used_processes(process_list: list):
    """Removes process from process list if they've been used up.

    Args:
        process_list (list): A list of ongoing processes.
    """
    for existing_process in process_list:
        if existing_process["volume"] == 0:
            process_list.remove(existing_process)


def save_tanks(tank_list: list):
    """Saves the updated tank list to the JSON file.

    Args:
        tank_list (list): A list of ongoing processes.
    """
    with open("resources/tanks.json", "w") as tanks_file:
        json.dump(tank_list, tanks_file, ensure_ascii=False, indent=4)


def save_processes(process_list: list):
    """Saves the updated process list to the JSON file.

    Args:
        process_list (list): A list of ongoing processes.
    """
    with open("resources/ongoing_processes.json", "w") as process_file:
        json.dump(process_list, process_file, ensure_ascii=False, indent=4)


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
        self.btn_send_bottles.clicked.connect(
            lambda: self.send_bottles_to_inventory(process_list))
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
        with open("resources/ongoing_processes.json", "r") as process_file:
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
        empty_tanks = []

        # Reads list showing tank availability.
        with open("resources/tanks.json", "r") as tanks_file:
            try:
                tank_list = json.load(tanks_file)
            except ValueError:
                print("Empty JSON file.")

        # Reads list of full tanks.
        with open("resources/tanks_original.json", "r") as orig_tanks_file:
            try:
                orig_tank_list = json.load(orig_tanks_file)
            except ValueError:
                print("Empty JSON file.")

        # Checks for full tanks.
        for tank in tank_list:
            for orig_tank in orig_tank_list:
                if tank["volume"] == orig_tank["volume"]:
                    any_empty_tank = True
                    empty_tanks.append(tank["tank"])
                    break

        # Gives advice on beer to brew if there's an empty tank.
        if any_empty_tank is True:
            # Finds the least stocked beer in inventory.
            (inventory_list, red_helles_volume, pilsner_volume,
             dunkel_volume) = InventoryManagementDialog.read_inventory(self)
            smallest_volume = min(
                red_helles_volume, pilsner_volume, dunkel_volume)
            if smallest_volume == red_helles_volume:
                recommend_brew = "Organic Red Helles"
            elif smallest_volume == pilsner_volume:
                recommend_brew = "Organic Pilsner"
            elif smallest_volume == dunkel_volume:
                recommend_brew = "Organic Dunkel"

            # Recommends the beer with the lowest stock.
            message = (recommend_brew + " should be brewed in the tank " +
                       empty_tanks[0] +
                       ", as it is currently the lowest in stock.")
            self.lbl_tank_advice.setText(message)

        return tank_list

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

    def send_bottles_to_inventory(self, process_list: list):
        """Removes finished bottling from process list and adds to inventory.

        Args:
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

                # Displays confirmation message of successful action.
                self.lbl_process_message.setText("Bottles successfully sent "
                                                 "to inventory.")

        # Saves the newly updated inventory.
        InventoryManagementDialog.save_inventory(inventory_list)
        # Saves the updated process list to the JSON file.
        save_processes(process_list)
        # Updates the process list in the UI.
        self.update_processes()

    def start_hot_brew(self, process_list: list):
        """Starts a hot brew for the given recipe and volume.

        Args:
            process_list (list): A list of ongoing processes.
        """
        new_volume = ""

        # Gets the inputs for the new process.
        try:
            new_recipe = self.combo_box_brew_recipe.currentText()
            new_volume = int(self.line_edit_brew_volume.text())
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if str(new_volume) != "":
            # Sets the completion date to three hours later.
            epoch_time = time() + 10800
            completion_date = strftime(
                "%d/%m/%Y %H:%M:%S", localtime(epoch_time))

            # Creates the process dictionary.
            process = {"process": "Hot Brew",
                       "recipe": new_recipe,
                       "tank": "N/A",
                       "volume": new_volume,
                       "completion": completion_date}

            # Appends the process to the process list.
            process_list.append(dict(process))

            # Displays confirmation message of successful action.
            self.lbl_process_message.setText("Hot brew successfully started.")

            # Saves the updated process list to the JSON file.
            save_processes(process_list)
            # Updates the process list in the UI.
            self.update_processes()

    def start_fermentation(self, tank_list: list, process_list: list):
        """Starts fermentation for the given recipe, tank, and volume.

        Args:
            tank_list (list): A list showing tank availability.
            process_list (list): A list of ongoing processes.
        """
        new_volume = ""

        # Gets the inputs for the new process.
        try:
            new_recipe = self.combo_box_ferment_recipe.currentText()
            new_tank = self.combo_box_ferment_tank.currentText()
            new_volume = int(self.line_edit_ferment_volume.text())
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if str(new_volume) != "":
            # Sets the completion date to four weeks later.
            epoch_time = time() + 2419200
            completion_date = strftime(
                "%d/%m/%Y %H:%M:%S", localtime(epoch_time))

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
                            existing_process["completion"],
                            "%d/%m/%Y %H:%M:%S")
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

                    # Displays confirmation message of successful action.
                    self.lbl_process_message.setText("Fermentation "
                                                     "successfully started.")
                    break

            # Removes process from process list if they've been used up.
            remove_used_processes(process_list)
            # Saves the updated tank list to the JSON file.
            save_tanks(tank_list)
            # Saves the updated process list to the JSON file.
            save_processes(process_list)
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
        new_volume = ""

        # Gets the inputs for the new process.
        try:
            new_recipe = self.combo_box_condition_recipe.currentText()
            new_tank = self.combo_box_condition_tank.currentText()
            new_volume = int(self.line_edit_condition_volume.text())
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if str(new_volume) != "":
            # Sets the completion date to two weeks later.
            epoch_time = time() + 1209600
            completion_date = strftime(
                "%d/%m/%Y %H:%M:%S", localtime(epoch_time))

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
                            existing_process["completion"],
                            "%d/%m/%Y %H:%M:%S")
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

                    # Displays confirmation message of successful action.
                    self.lbl_process_message.setText("Conditioning "
                                                     "successfully started.")
                    break

            # Removes process from process list if they've been used up.
            remove_used_processes(process_list)
            # Saves the updated tank list to the JSON file.
            save_tanks(tank_list)
            # Saves the updated process list to the JSON file.
            save_processes(process_list)
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
        new_volume = ""

        # Gets the inputs for the new process.
        try:
            new_recipe = self.combo_box_bottle_recipe.currentText()
            new_volume = int(self.line_edit_bottle_volume.text())
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if str(new_volume) != "":
            # Sets the completion date to 10 minutes per bottle later.
            epoch_time = time() + ((new_volume / 0.5) * 600)
            completion_date = strftime("%d/%m/%Y %H:%M:%S",
                                       localtime(epoch_time))

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
                            existing_process["completion"],
                            "%d/%m/%Y %H:%M:%S")
                        <= datetime.now()):
                    # Adds process details to the list.
                    process_list.append(dict(process))

                    for tank in tank_list:
                        # Adds volume to tank of prerequisite.
                        if tank["tank"] == existing_process["tank"]:
                            tank["volume"] += new_volume

                    # Removes volume from the prerequisite process.
                    existing_process["volume"] -= new_volume

                    # Displays confirmation message of successful action.
                    self.lbl_process_message.setText("Bottling "
                                                     "successfully started.")
                    break

            # Removes process from process list if they've been used up.
            remove_used_processes(process_list)
            # Saves the updated tank list to the JSON file.
            save_tanks(tank_list)
            # Saves the updated process list to the JSON file.
            save_processes(process_list)
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
        abort_volume = ""

        # Gets the inputs for the process to abort.
        try:
            abort_process = self.combo_box_abort_process.currentText()
            abort_recipe = self.combo_box_abort_recipe.currentText()
            abort_tank = self.combo_box_abort_tank.currentText()
            abort_volume = int(self.line_edit_abort_volume.text())
            abort_completion = self.date_time_edit_completion.text()
        except (ValueError, TypeError):
            pass

        # Validates against null input.
        if abort_volume != "":
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

                    # Displays confirmation message of successful action.
                    self.lbl_process_message.setText("Process "
                                                     "successfully aborted.")

            # Saves the updated tank list to the JSON file.
            save_tanks(tank_list)
            # Saves the updated process list to the JSON file.
            save_processes(process_list)
            # Updates the tank availability displayed in the UI.
            self.update_tanks()
            # Updates the process list in the UI.
            self.update_processes()
