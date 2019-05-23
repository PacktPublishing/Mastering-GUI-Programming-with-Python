# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calendar_form.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(799, 600)
        self.horizontalLayout = QtWidgets.QHBoxLayout(MainWindow)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.calendar = QtWidgets.QCalendarWidget(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendar.sizePolicy().hasHeightForWidth())
        self.calendar.setSizePolicy(sizePolicy)
        self.calendar.setObjectName("calendar")
        self.horizontalLayout.addWidget(self.calendar)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(MainWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.event_list = QtWidgets.QListWidget(MainWindow)
        self.event_list.setObjectName("event_list")
        self.verticalLayout.addWidget(self.event_list)
        self.groupBox = QtWidgets.QGroupBox(MainWindow)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.event_category = QtWidgets.QComboBox(self.groupBox)
        self.event_category.setObjectName("event_category")
        self.event_category.addItem("")
        self.event_category.addItem("")
        self.event_category.addItem("")
        self.event_category.addItem("")
        self.event_category.addItem("")
        self.event_category.addItem("")
        self.gridLayout.addWidget(self.event_category, 1, 0, 1, 1)
        self.event_time = QtWidgets.QTimeEdit(self.groupBox)
        self.event_time.setObjectName("event_time")
        self.gridLayout.addWidget(self.event_time, 1, 1, 1, 1)
        self.event_detail = QtWidgets.QTextEdit(self.groupBox)
        self.event_detail.setObjectName("event_detail")
        self.gridLayout.addWidget(self.event_detail, 2, 0, 1, 3)
        self.event_title = QtWidgets.QLineEdit(self.groupBox)
        self.event_title.setObjectName("event_title")
        self.gridLayout.addWidget(self.event_title, 0, 0, 1, 3)
        self.allday_check = QtWidgets.QCheckBox(self.groupBox)
        self.allday_check.setObjectName("allday_check")
        self.gridLayout.addWidget(self.allday_check, 1, 2, 1, 1)
        self.add_button = QtWidgets.QPushButton(self.groupBox)
        self.add_button.setObjectName("add_button")
        self.gridLayout.addWidget(self.add_button, 3, 1, 1, 1)
        self.del_button = QtWidgets.QPushButton(self.groupBox)
        self.del_button.setObjectName("del_button")
        self.gridLayout.addWidget(self.del_button, 3, 2, 1, 1)
        self.verticalLayout.addWidget(self.groupBox)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(MainWindow)
        self.allday_check.toggled['bool'].connect(self.event_time.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "My Calendar App"))
        self.label.setText(_translate("MainWindow", "Events on Date"))
        self.groupBox.setTitle(_translate("MainWindow", "Event"))
        self.event_category.setItemText(0, _translate("MainWindow", "Select Category…"))
        self.event_category.setItemText(1, _translate("MainWindow", "New…"))
        self.event_category.setItemText(2, _translate("MainWindow", "Work"))
        self.event_category.setItemText(3, _translate("MainWindow", "Meeting"))
        self.event_category.setItemText(4, _translate("MainWindow", "Doctor"))
        self.event_category.setItemText(5, _translate("MainWindow", "Family"))
        self.allday_check.setText(_translate("MainWindow", "All Day"))
        self.add_button.setText(_translate("MainWindow", "Add/Update"))
        self.del_button.setText(_translate("MainWindow", "Delete"))

