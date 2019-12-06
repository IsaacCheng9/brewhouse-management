"""
The base user interface for the dialog for uploading new sales data.

This creates the objects in the user interface, so that the user can interact
with the program more easily.

Coding: utf-8
Form implementation generated from reading ui file 'upload_sales.ui'
Created by: PyQt5 UI code generator 5.13.1
"""


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_upload_sales(object):
    def setupUi(self, dialog_upload_sales):
        dialog_upload_sales.setObjectName("dialog_upload_sales")
        dialog_upload_sales.resize(600, 375)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        dialog_upload_sales.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(dialog_upload_sales)
        self.gridLayout.setObjectName("gridLayout")
        self.scroll_area = QtWidgets.QScrollArea(dialog_upload_sales)
        font = QtGui.QFont()
        font.setKerning(True)
        self.scroll_area.setFont(font)
        self.scroll_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_area.setFrameShadow(QtWidgets.QFrame.Plain)
        self.scroll_area.setLineWidth(0)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("scroll_area")
        self.scroll_area_widget_contents = QtWidgets.QWidget()
        self.scroll_area_widget_contents.setGeometry(
            QtCore.QRect(0, 0, 578, 353))
        self.scroll_area_widget_contents.setObjectName(
            "scroll_area_widget_contents")
        self.verticalLayoutWidget = QtWidgets.QWidget(
            self.scroll_area_widget_contents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 571, 331))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vert_layout_upload_sales = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.vert_layout_upload_sales.setContentsMargins(0, 0, 0, 0)
        self.vert_layout_upload_sales.setObjectName("vert_layout_upload_sales")
        self.lbl_upload_sales = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setKerning(True)
        self.lbl_upload_sales.setFont(font)
        self.lbl_upload_sales.setObjectName("lbl_upload_sales")
        self.vert_layout_upload_sales.addWidget(self.lbl_upload_sales)
        self.hori_line_upload_sales = QtWidgets.QFrame(
            self.verticalLayoutWidget)
        self.hori_line_upload_sales.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_upload_sales.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_upload_sales.setObjectName("hori_line_upload_sales")
        self.vert_layout_upload_sales.addWidget(self.hori_line_upload_sales)
        self.grid_layout_upload_sales = QtWidgets.QGridLayout()
        self.grid_layout_upload_sales.setObjectName("grid_layout_upload_sales")
        self.lbl_sale_date = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_date.setObjectName("lbl_sale_date")
        self.grid_layout_upload_sales.addWidget(self.lbl_sale_date, 3, 0, 1, 1)
        self.date_edit_sale_date = QtWidgets.QDateEdit(
            self.verticalLayoutWidget)
        self.date_edit_sale_date.setDateTime(QtCore.QDateTime(
            QtCore.QDate(2019, 11, 1), QtCore.QTime(0, 0, 0)))
        self.date_edit_sale_date.setMaximumDateTime(QtCore.QDateTime(
            QtCore.QDate(9999, 1, 1), QtCore.QTime(23, 59, 59)))
        self.date_edit_sale_date.setMinimumDateTime(
            QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.date_edit_sale_date.setMaximumDate(QtCore.QDate(9999, 1, 1))
        self.date_edit_sale_date.setCalendarPopup(True)
        self.date_edit_sale_date.setObjectName("date_edit_sale_date")
        self.grid_layout_upload_sales.addWidget(
            self.date_edit_sale_date, 3, 1, 1, 1)
        self.lbl_sale_recipe = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_recipe.setObjectName("lbl_sale_recipe")
        self.grid_layout_upload_sales.addWidget(
            self.lbl_sale_recipe, 4, 0, 1, 1)
        self.combo_box_sale_recipe = QtWidgets.QComboBox(
            self.verticalLayoutWidget)
        self.combo_box_sale_recipe.setObjectName("combo_box_sale_recipe")
        self.combo_box_sale_recipe.addItem("")
        self.combo_box_sale_recipe.addItem("")
        self.combo_box_sale_recipe.addItem("")
        self.grid_layout_upload_sales.addWidget(
            self.combo_box_sale_recipe, 4, 1, 1, 1)
        self.lbl_sale_quantity = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_quantity.setObjectName("lbl_sale_quantity")
        self.grid_layout_upload_sales.addWidget(
            self.lbl_sale_quantity, 6, 0, 1, 1)
        self.line_edit_sale_quantity = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_sale_quantity.setMaxLength(13)
        self.line_edit_sale_quantity.setObjectName("line_edit_sale_quantity")
        self.grid_layout_upload_sales.addWidget(
            self.line_edit_sale_quantity, 6, 1, 1, 1)
        self.lbl_sale_invoice = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_invoice.setObjectName("lbl_sale_invoice")
        self.grid_layout_upload_sales.addWidget(
            self.lbl_sale_invoice, 1, 0, 1, 1)
        self.line_edit_sale_invoice = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_sale_invoice.setMaxLength(13)
        self.line_edit_sale_invoice.setObjectName("line_edit_sale_invoice")
        self.grid_layout_upload_sales.addWidget(
            self.line_edit_sale_invoice, 1, 1, 1, 1)
        self.lbl_sale_customer = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_customer.setObjectName("lbl_sale_customer")
        self.grid_layout_upload_sales.addWidget(
            self.lbl_sale_customer, 2, 0, 1, 1)
        self.line_edit_sale_customer = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_sale_customer.setMaxLength(40)
        self.line_edit_sale_customer.setObjectName("line_edit_sale_customer")
        self.grid_layout_upload_sales.addWidget(
            self.line_edit_sale_customer, 2, 1, 1, 1)
        self.lbl_sale_gyle = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_sale_gyle.setObjectName("lbl_sale_gyle")
        self.grid_layout_upload_sales.addWidget(self.lbl_sale_gyle, 5, 0, 1, 1)
        self.line_edit_sale_gyle = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_sale_gyle.setMaxLength(13)
        self.line_edit_sale_gyle.setObjectName("line_edit_sale_gyle")
        self.grid_layout_upload_sales.addWidget(
            self.line_edit_sale_gyle, 5, 1, 1, 1)
        self.vert_layout_upload_sales.addLayout(self.grid_layout_upload_sales)
        self.btn_upload_sale = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_upload_sale.setObjectName("btn_upload_sale")
        self.vert_layout_upload_sales.addWidget(
            self.btn_upload_sale, 0, QtCore.Qt.AlignLeft)
        self.hori_line_sale = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_sale.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_sale.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_sale.setObjectName("hori_line_sale")
        self.vert_layout_upload_sales.addWidget(self.hori_line_sale)
        self.lbl_upload_successful = QtWidgets.QLabel(
            self.verticalLayoutWidget)
        self.lbl_upload_successful.setText("")
        self.lbl_upload_successful.setObjectName("lbl_upload_successful")
        self.vert_layout_upload_sales.addWidget(self.lbl_upload_successful)
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.vert_layout_upload_sales.addItem(spacerItem)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.gridLayout.addWidget(self.scroll_area, 0, 0, 1, 1)

        self.retranslateUi(dialog_upload_sales)
        QtCore.QMetaObject.connectSlotsByName(dialog_upload_sales)

    def retranslateUi(self, dialog_upload_sales):
        _translate = QtCore.QCoreApplication.translate
        dialog_upload_sales.setWindowTitle(_translate(
            "dialog_upload_sales",
            "Upload New Sales Data - Barnaby\'s Brewhouse"))
        self.lbl_upload_sales.setText(_translate(
            "dialog_upload_sales", "Upload New Sales Data"))
        self.lbl_sale_date.setText(_translate(
            "dialog_upload_sales", "Date Required:"))
        self.lbl_sale_recipe.setText(
            _translate("dialog_upload_sales", "Recipe:"))
        self.combo_box_sale_recipe.setItemText(
            0, _translate("dialog_upload_sales", "Organic Red Helles"))
        self.combo_box_sale_recipe.setItemText(
            1, _translate("dialog_upload_sales", "Organic Pilsner"))
        self.combo_box_sale_recipe.setItemText(
            2, _translate("dialog_upload_sales", "Organic Dunkel"))
        self.lbl_sale_quantity.setText(_translate(
            "dialog_upload_sales", "Quantity Ordered:"))
        self.lbl_sale_invoice.setText(_translate(
            "dialog_upload_sales", "Invoice Number:"))
        self.lbl_sale_customer.setText(
            _translate("dialog_upload_sales", "Customer:"))
        self.lbl_sale_gyle.setText(_translate(
            "dialog_upload_sales", "Gyle Number:"))
        self.btn_upload_sale.setText(_translate(
            "dialog_upload_sales", "Upload New Sale"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_upload_sales = QtWidgets.QDialog()
    ui = Ui_dialog_upload_sales()
    ui.setupUi(dialog_upload_sales)
    dialog_upload_sales.show()
    sys.exit(app.exec_())
