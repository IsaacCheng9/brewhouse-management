# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'brewhouse.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 720)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 289, 309))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lbl_brewhouse = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.lbl_brewhouse.setFont(font)
        self.lbl_brewhouse.setObjectName("lbl_brewhouse")
        self.verticalLayout.addWidget(self.lbl_brewhouse)
        self.hori_line_brewhouse = QtWidgets.QFrame(self.layoutWidget)
        self.hori_line_brewhouse.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_brewhouse.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_brewhouse.setObjectName("hori_line_brewhouse")
        self.verticalLayout.addWidget(self.hori_line_brewhouse)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btn_predict = QtWidgets.QPushButton(self.layoutWidget)
        self.btn_predict.setObjectName("btn_predict")
        self.horizontalLayout_2.addWidget(self.btn_predict)
        self.pushButton_2 = QtWidgets.QPushButton(self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.hori_line_nav = QtWidgets.QFrame(self.layoutWidget)
        self.hori_line_nav.setFrameShape(QtWidgets.QFrame.HLine)
        self.hori_line_nav.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.hori_line_nav.setObjectName("hori_line_nav")
        self.verticalLayout.addWidget(self.hori_line_nav)
        self.lbl_sales_ratios = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lbl_sales_ratios.setFont(font)
        self.lbl_sales_ratios.setObjectName("lbl_sales_ratios")
        self.verticalLayout.addWidget(self.lbl_sales_ratios)
        self.lbl_red_helles_ratio = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_red_helles_ratio.setObjectName("lbl_red_helles_ratio")
        self.verticalLayout.addWidget(self.lbl_red_helles_ratio)
        self.lbl_pilsner_ratio = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_pilsner_ratio.setObjectName("lbl_pilsner_ratio")
        self.verticalLayout.addWidget(self.lbl_pilsner_ratio)
        self.lbl_dunkel_ratio = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_dunkel_ratio.setObjectName("lbl_dunkel_ratio")
        self.verticalLayout.addWidget(self.lbl_dunkel_ratio)
        self.line = QtWidgets.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)
        self.lbl_sales_ratios_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setUnderline(True)
        self.lbl_sales_ratios_2.setFont(font)
        self.lbl_sales_ratios_2.setObjectName("lbl_sales_ratios_2")
        self.verticalLayout.addWidget(self.lbl_sales_ratios_2)
        self.lbl_red_helles_ratio_2 = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_red_helles_ratio_2.setObjectName("lbl_red_helles_ratio_2")
        self.verticalLayout.addWidget(self.lbl_red_helles_ratio_2)
        self.lbl_red_helles_ratio_3 = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_red_helles_ratio_3.setObjectName("lbl_red_helles_ratio_3")
        self.verticalLayout.addWidget(self.lbl_red_helles_ratio_3)
        self.lbl_red_helles_ratio_4 = QtWidgets.QLabel(self.layoutWidget)
        self.lbl_red_helles_ratio_4.setObjectName("lbl_red_helles_ratio_4")
        self.verticalLayout.addWidget(self.lbl_red_helles_ratio_4)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lbl_brewhouse.setText(_translate(
            "MainWindow", "Barnaby\'s Brewhouse"))
        self.btn_predict.setText(_translate("MainWindow", "Predict Sales"))
        self.pushButton_2.setText(_translate(
            "MainWindow", "Process Monitoring"))
        self.lbl_sales_ratios.setText(_translate("MainWindow", "Sales Ratios"))
        self.lbl_red_helles_ratio.setText(
            _translate("MainWindow", "Organic Red Helles - "))
        self.lbl_pilsner_ratio.setText(
            _translate("MainWindow", "Organic Pilsner - "))
        self.lbl_dunkel_ratio.setText(
            _translate("MainWindow", "Organic Dunkel - "))
        self.lbl_sales_ratios_2.setText(_translate(
            "MainWindow", "Average Monthly Growth Percentages"))
        self.lbl_red_helles_ratio_2.setText(
            _translate("MainWindow", "Organic Red Helles - "))
        self.lbl_red_helles_ratio_3.setText(
            _translate("MainWindow", "Organic Pilsner  - "))
        self.lbl_red_helles_ratio_4.setText(
            _translate("MainWindow", "Organic Dunkel - "))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
