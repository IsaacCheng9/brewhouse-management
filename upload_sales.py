"""
A system which provides the user with a form they can fill to upload a new sale
to the sales data CSV file.
"""

from datetime import datetime

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QDialog

from upload_sales_setup import Ui_dialog_upload_sales


class UploadSalesDialog(QDialog, Ui_dialog_upload_sales):
    """Contains the dialog window for uploading new sales data."""

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Restricts inputs to only numbers.
        self.only_int = QIntValidator()
        self.line_edit_sale_invoice.setValidator(self.only_int)
        self.line_edit_sale_gyle.setValidator(self.only_int)
        self.line_edit_sale_quantity.setValidator(self.only_int)

        # Connects the 'Upload New Sale' button to add the inputted sale.
        self.btn_upload_sale.clicked.connect(self.upload_sale)

    def upload_sale(self):
        """Uploads the new sale to the sales data CSV file."""
        # Gets the inputs for the new sale.
        invoice = self.line_edit_sale_invoice.text()
        customer = self.line_edit_sale_customer.text()
        date = self.date_edit_sale_date.text()
        recipe = self.combo_box_sale_recipe.currentText()
        gyle = self.line_edit_sale_gyle.text()
        quantity = self.line_edit_sale_quantity.text()

        # Validates against null inputs.
        if (invoice != "" and customer != "" and gyle != "" and
                quantity != ""):
            # Writes new sales data to the CSV file.
            with open("sales_data.csv", "a") as sales_file:
                date = datetime.strptime(date, "%d/%m/%Y").strftime("%d-%b-%y")
                sale = (invoice + "," + customer + "," + date + "," + recipe +
                        "," + gyle + "," + quantity + "\n")
                sales_file.write(sale)
            # Notifies the user that their upload was successful.
            self.lbl_upload_successful.setText("Sale uploaded successfully!")
        else:
            # Notifies the user that their  upload was unsuccessful.
            self.lbl_upload_successful.setText(
                "This is not a valid sale. Please fill all input fields to "
                "upload your sale.")
