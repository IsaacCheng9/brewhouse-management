"""
The base user interface for the dialog for inventory management.

This creates the objects in the user interface, so that the user can interact
with the program more easily.

Coding: utf-8
Form implementation generated from reading ui file 'inv_management.ui'
Created by: PyQt5 UI code generator 5.13.1
"""


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_dialog_inv_management(object):
    """Creates the objects for the UI of this dialog for managing inventory."""
    def setupUi(self, dialog_inv_management):
        dialog_inv_management.setObjectName("dialog_inv_management")
        dialog_inv_management.resize(800, 800)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        dialog_inv_management.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(dialog_inv_management)
        self.gridLayout.setObjectName("gridLayout")
        self.scroll_area = QtWidgets.QScrollArea(dialog_inv_management)
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
            QtCore.QRect(0, 0, 778, 778))
        self.scroll_area_widget_contents.setObjectName(
            "scroll_area_widget_contents")
        self.verticalLayoutWidget = QtWidgets.QWidget(
            self.scroll_area_widget_contents)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 771, 771))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.vert_layout_inv_management = QtWidgets.QVBoxLayout(
            self.verticalLayoutWidget)
        self.vert_layout_inv_management.setContentsMargins(0, 0, 0, 0)
        self.vert_layout_inv_management.setObjectName(
            "vert_layout_inv_management")
        self.lbl_inv_management = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        font.setKerning(True)
        self.lbl_inv_management.setFont(font)
        self.lbl_inv_management.setObjectName("lbl_inv_management")
        self.vert_layout_inv_management.addWidget(self.lbl_inv_management)
        self.hori_line_monitoring = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_monitoring.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_monitoring.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_monitoring.setObjectName("hori_line_monitoring")
        self.vert_layout_inv_management.addWidget(self.hori_line_monitoring)
        self.lbl_inv = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setKerning(True)
        self.lbl_inv.setFont(font)
        self.lbl_inv.setObjectName("lbl_inv")
        self.vert_layout_inv_management.addWidget(self.lbl_inv)
        self.lbl_red_helles_inv = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_red_helles_inv.setObjectName("lbl_red_helles_inv")
        self.vert_layout_inv_management.addWidget(self.lbl_red_helles_inv)
        self.lbl_pilsner_inv = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_pilsner_inv.setObjectName("lbl_pilsner_inv")
        self.vert_layout_inv_management.addWidget(self.lbl_pilsner_inv)
        self.lbl_dunkel_inv = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_dunkel_inv.setObjectName("lbl_dunkel_inv")
        self.vert_layout_inv_management.addWidget(self.lbl_dunkel_inv)
        self.hori_line_inv = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_inv.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_inv.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_inv.setObjectName("hori_line_inv")
        self.vert_layout_inv_management.addWidget(self.hori_line_inv)
        self.lbl_update_inv = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setKerning(True)
        self.lbl_update_inv.setFont(font)
        self.lbl_update_inv.setObjectName("lbl_update_inv")
        self.vert_layout_inv_management.addWidget(self.lbl_update_inv)
        self.grid_layout_update_inv = QtWidgets.QGridLayout()
        self.grid_layout_update_inv.setObjectName("grid_layout_update_inv")
        self.lbl_update_inv_volume = QtWidgets.QLabel(
            self.verticalLayoutWidget)
        self.lbl_update_inv_volume.setObjectName("lbl_update_inv_volume")
        self.grid_layout_update_inv.addWidget(
            self.lbl_update_inv_volume, 2, 0, 1, 1)
        self.lbl_update_inv_recipe = QtWidgets.QLabel(
            self.verticalLayoutWidget)
        self.lbl_update_inv_recipe.setObjectName("lbl_update_inv_recipe")
        self.grid_layout_update_inv.addWidget(
            self.lbl_update_inv_recipe, 1, 0, 1, 1)
        self.combo_box_update_inv_recipe = QtWidgets.QComboBox(
            self.verticalLayoutWidget)
        self.combo_box_update_inv_recipe.setObjectName(
            "combo_box_update_inv_recipe")
        self.combo_box_update_inv_recipe.addItem("")
        self.combo_box_update_inv_recipe.addItem("")
        self.combo_box_update_inv_recipe.addItem("")
        self.grid_layout_update_inv.addWidget(
            self.combo_box_update_inv_recipe, 1, 1, 1, 1)
        self.line_edit_update_inv_volume = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_update_inv_volume.setMaxLength(13)
        self.line_edit_update_inv_volume.setObjectName(
            "line_edit_update_inv_volume")
        self.grid_layout_update_inv.addWidget(
            self.line_edit_update_inv_volume, 2, 1, 1, 1)
        self.vert_layout_inv_management.addLayout(self.grid_layout_update_inv)
        self.hori_layout_update_inv = QtWidgets.QHBoxLayout()
        self.hori_layout_update_inv.setObjectName("hori_layout_update_inv")
        self.btn_add_inv = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_add_inv.setObjectName("btn_add_inv")
        self.hori_layout_update_inv.addWidget(self.btn_add_inv)
        self.btn_remove_inv = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_remove_inv.setObjectName("btn_remove_inv")
        self.hori_layout_update_inv.addWidget(self.btn_remove_inv)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.hori_layout_update_inv.addItem(spacerItem)
        self.vert_layout_inv_management.addLayout(self.hori_layout_update_inv)
        self.hori_line_update_inv = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_update_inv.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_update_inv.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_update_inv.setObjectName("hori_line_update_inv")
        self.vert_layout_inv_management.addWidget(self.hori_line_update_inv)
        self.lbl_customer_orders = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setKerning(True)
        self.lbl_customer_orders.setFont(font)
        self.lbl_customer_orders.setObjectName("lbl_customer_orders")
        self.vert_layout_inv_management.addWidget(self.lbl_customer_orders)
        self.lbl_orders = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_orders.setText("")
        self.lbl_orders.setObjectName("lbl_orders")
        self.vert_layout_inv_management.addWidget(self.lbl_orders)
        self.hori_line_orders = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_orders.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_orders.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_orders.setObjectName("hori_line_orders")
        self.vert_layout_inv_management.addWidget(self.hori_line_orders)
        self.lbl_add_order = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setKerning(True)
        self.lbl_add_order.setFont(font)
        self.lbl_add_order.setObjectName("lbl_add_order")
        self.vert_layout_inv_management.addWidget(self.lbl_add_order)
        self.grid_layout_add_order = QtWidgets.QGridLayout()
        self.grid_layout_add_order.setObjectName("grid_layout_add_order")
        self.lbl_add_order_recipe = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_add_order_recipe.setObjectName("lbl_add_order_recipe")
        self.grid_layout_add_order.addWidget(
            self.lbl_add_order_recipe, 2, 0, 1, 1)
        self.combo_box_add_order_recipe = QtWidgets.QComboBox(
            self.verticalLayoutWidget)
        self.combo_box_add_order_recipe.setObjectName(
            "combo_box_add_order_recipe")
        self.combo_box_add_order_recipe.addItem("")
        self.combo_box_add_order_recipe.addItem("")
        self.combo_box_add_order_recipe.addItem("")
        self.grid_layout_add_order.addWidget(
            self.combo_box_add_order_recipe, 2, 1, 1, 1)
        self.line_edit_add_order_volume = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_add_order_volume.setMaxLength(13)
        self.line_edit_add_order_volume.setObjectName(
            "line_edit_add_order_volume")
        self.grid_layout_add_order.addWidget(
            self.line_edit_add_order_volume, 3, 1, 1, 1)
        self.lbl_add_order_volume = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_add_order_volume.setObjectName("lbl_add_order_volume")
        self.grid_layout_add_order.addWidget(
            self.lbl_add_order_volume, 3, 0, 1, 1)
        self.lbl_add_order_id = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_add_order_id.setObjectName("lbl_add_order_id")
        self.grid_layout_add_order.addWidget(self.lbl_add_order_id, 1, 0, 1, 1)
        self.line_edit_add_order_id = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_add_order_id.setMaxLength(13)
        self.line_edit_add_order_id.setObjectName("line_edit_add_order_id")
        self.grid_layout_add_order.addWidget(
            self.line_edit_add_order_id, 1, 1, 1, 1)
        self.vert_layout_inv_management.addLayout(self.grid_layout_add_order)
        self.btn_add_order = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.btn_add_order.setObjectName("btn_add_order")
        self.vert_layout_inv_management.addWidget(
            self.btn_add_order, 0, QtCore.Qt.AlignLeft)
        self.hori_line_add_order = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.hori_line_add_order.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_add_order.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_add_order.setObjectName("hori_line_add_order")
        self.vert_layout_inv_management.addWidget(self.hori_line_add_order)
        self.lbl_dispatch_order = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        font.setKerning(True)
        self.lbl_dispatch_order.setFont(font)
        self.lbl_dispatch_order.setObjectName("lbl_dispatch_order")
        self.vert_layout_inv_management.addWidget(self.lbl_dispatch_order)
        self.hori_layout_dispatch_order = QtWidgets.QHBoxLayout()
        self.hori_layout_dispatch_order.setObjectName(
            "hori_layout_dispatch_order")
        self.lbl_dispatch_order_id = QtWidgets.QLabel(
            self.verticalLayoutWidget)
        self.lbl_dispatch_order_id.setObjectName("lbl_dispatch_order_id")
        self.hori_layout_dispatch_order.addWidget(
            self.lbl_dispatch_order_id, 0, QtCore.Qt.AlignLeft)
        self.line_edit_dispatch_order_id = QtWidgets.QLineEdit(
            self.verticalLayoutWidget)
        self.line_edit_dispatch_order_id.setMaxLength(13)
        self.line_edit_dispatch_order_id.setObjectName(
            "line_edit_dispatch_order_id")
        self.hori_layout_dispatch_order.addWidget(
            self.line_edit_dispatch_order_id, 0, QtCore.Qt.AlignLeft)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding,
            QtWidgets.QSizePolicy.Minimum)
        self.hori_layout_dispatch_order.addItem(spacerItem1)
        self.vert_layout_inv_management.addLayout(
            self.hori_layout_dispatch_order)
        self.btn_dispatch_order = QtWidgets.QPushButton(
            self.verticalLayoutWidget)
        self.btn_dispatch_order.setObjectName("btn_dispatch_order")
        self.vert_layout_inv_management.addWidget(
            self.btn_dispatch_order, 0, QtCore.Qt.AlignLeft)
        self.hori_line_dispatch_order = QtWidgets.QFrame(
            self.verticalLayoutWidget)
        self.hori_line_dispatch_order.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_dispatch_order.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_dispatch_order.setObjectName("hori_line_dispatch_order")
        self.vert_layout_inv_management.addWidget(
            self.hori_line_dispatch_order)
        self.lbl_order_message = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.lbl_order_message.setObjectName("lbl_order_message")
        self.vert_layout_inv_management.addWidget(self.lbl_order_message)
        spacerItem2 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum,
            QtWidgets.QSizePolicy.Expanding)
        self.vert_layout_inv_management.addItem(spacerItem2)
        self.scroll_area.setWidget(self.scroll_area_widget_contents)
        self.gridLayout.addWidget(self.scroll_area, 0, 0, 1, 1)

        self.retranslateUi(dialog_inv_management)
        QtCore.QMetaObject.connectSlotsByName(dialog_inv_management)

    def retranslateUi(self, dialog_inv_management):
        _translate = QtCore.QCoreApplication.translate
        dialog_inv_management.setWindowTitle(_translate(
            "dialog_inv_management",
            "Inventory Management - Barnaby\'s Brewhouse"))
        self.lbl_inv_management.setText(_translate(
            "dialog_inv_management", "Inventory Management"))
        self.lbl_inv.setText(_translate("dialog_inv_management", "Inventory"))
        self.lbl_red_helles_inv.setText(_translate(
            "dialog_inv_management", "Organic Red Helles: "))
        self.lbl_pilsner_inv.setText(_translate(
            "dialog_inv_management", "Organic Pilsner: "))
        self.lbl_dunkel_inv.setText(_translate(
            "dialog_inv_management", "Organic Dunkel: "))
        self.lbl_update_inv.setText(_translate(
            "dialog_inv_management", "Update Inventory"))
        self.lbl_update_inv_volume.setText(
            _translate("dialog_inv_management", "Volume (L):"))
        self.lbl_update_inv_recipe.setText(
            _translate("dialog_inv_management", "Beer Recipe:"))
        self.combo_box_update_inv_recipe.setItemText(
            0, _translate("dialog_inv_management", "Organic Red Helles"))
        self.combo_box_update_inv_recipe.setItemText(
            1, _translate("dialog_inv_management", "Organic Pilsner"))
        self.combo_box_update_inv_recipe.setItemText(
            2, _translate("dialog_inv_management", "Organic Dunkel"))
        self.btn_add_inv.setText(_translate(
            "dialog_inv_management", "Add to Inventory"))
        self.btn_remove_inv.setText(_translate(
            "dialog_inv_management", "Remove from Inventory"))
        self.lbl_customer_orders.setText(_translate(
            "dialog_inv_management", "Customer Orders"))
        self.lbl_add_order.setText(_translate(
            "dialog_inv_management", "Add Customer Order"))
        self.lbl_add_order_recipe.setText(_translate(
            "dialog_inv_management", "Beer Recipe:"))
        self.combo_box_add_order_recipe.setItemText(
            0, _translate("dialog_inv_management", "Organic Red Helles"))
        self.combo_box_add_order_recipe.setItemText(
            1, _translate("dialog_inv_management", "Organic Pilsner"))
        self.combo_box_add_order_recipe.setItemText(
            2, _translate("dialog_inv_management", "Organic Dunkel"))
        self.lbl_add_order_volume.setText(
            _translate("dialog_inv_management", "Volume (L):"))
        self.lbl_add_order_id.setText(_translate(
            "dialog_inv_management", "Order ID:"))
        self.btn_add_order.setText(_translate(
            "dialog_inv_management", "Add Order"))
        self.lbl_dispatch_order.setText(_translate(
            "dialog_inv_management", "Dispatch Customer Order"))
        self.lbl_dispatch_order_id.setText(
            _translate("dialog_inv_management", "Order ID:"))
        self.btn_dispatch_order.setText(_translate(
            "dialog_inv_management", "Dispatch Order"))
        self.lbl_order_message.setText(
            _translate("dialog_inv_management", " "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    dialog_inv_management = QtWidgets.QDialog()
    ui = Ui_dialog_inv_management()
    ui.setupUi(dialog_inv_management)
    dialog_inv_management.show()
    sys.exit(app.exec_())
