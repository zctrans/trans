# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui/ui/gui_dropconn.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(559, 515)
        MainWindow.setStyleSheet("QLabel {\n"
"    border: 1px solid black;\n"
"    border-radius: 6px;\n"
"    padding: 3px;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gateway_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.gateway_edit.setGeometry(QtCore.QRect(110, 20, 231, 23))
        self.gateway_edit.setObjectName("gateway_edit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label.setObjectName("label")
        self.floor_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.floor_edit.setGeometry(QtCore.QRect(110, 60, 41, 23))
        self.floor_edit.setObjectName("floor_edit")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.label_2.setObjectName("label_2")
        self.ceil_edit = QtWidgets.QLineEdit(self.centralwidget)
        self.ceil_edit.setGeometry(QtCore.QRect(260, 60, 41, 23))
        self.ceil_edit.setObjectName("ceil_edit")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(160, 60, 91, 21))
        self.label_3.setObjectName("label_3")
        self.victims_list = QtWidgets.QListView(self.centralwidget)
        self.victims_list.setGeometry(QtCore.QRect(10, 90, 256, 321))
        self.victims_list.setObjectName("victims_list")
        self.drop_button = QtWidgets.QPushButton(self.centralwidget)
        self.drop_button.setGeometry(QtCore.QRect(20, 420, 80, 23))
        self.drop_button.setObjectName("drop_button")
        self.scan_button = QtWidgets.QPushButton(self.centralwidget)
        self.scan_button.setGeometry(QtCore.QRect(270, 90, 31, 321))
        self.scan_button.setText("")
        self.scan_button.setObjectName("scan_button")
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(310, 90, 201, 321))
        self.status_label.setText("")
        self.status_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.status_label.setObjectName("status_label")
        self.stop_button = QtWidgets.QPushButton(self.centralwidget)
        self.stop_button.setGeometry(QtCore.QRect(20, 450, 80, 23))
        self.stop_button.setObjectName("stop_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Gateway IP:"))
        self.label_2.setText(_translate("MainWindow", "Scan floor:"))
        self.label_3.setText(_translate("MainWindow", "Scan ceil:"))
        self.drop_button.setText(_translate("MainWindow", "DROP"))
        self.stop_button.setText(_translate("MainWindow", "Stop"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
