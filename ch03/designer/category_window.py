# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'category_window.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CategoryWindow(object):
    def setupUi(self, CategoryWindow):
        CategoryWindow.setObjectName("CategoryWindow")
        CategoryWindow.setWindowModality(QtCore.Qt.WindowModal)
        CategoryWindow.resize(409, 120)
        self.verticalLayout = QtWidgets.QVBoxLayout(CategoryWindow)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(CategoryWindow)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.category_entry = QtWidgets.QLineEdit(CategoryWindow)
        self.category_entry.setObjectName("category_entry")
        self.verticalLayout.addWidget(self.category_entry)
        self.submit_btn = QtWidgets.QPushButton(CategoryWindow)
        self.submit_btn.setObjectName("submit_btn")
        self.verticalLayout.addWidget(self.submit_btn)
        self.cancel_btn = QtWidgets.QPushButton(CategoryWindow)
        self.cancel_btn.setObjectName("cancel_btn")
        self.verticalLayout.addWidget(self.cancel_btn)

        self.retranslateUi(CategoryWindow)
        QtCore.QMetaObject.connectSlotsByName(CategoryWindow)

    def retranslateUi(self, CategoryWindow):
        _translate = QtCore.QCoreApplication.translate
        CategoryWindow.setWindowTitle(_translate("CategoryWindow", "Form"))
        self.label.setText(_translate("CategoryWindow", "Please enter a new category name:"))
        self.submit_btn.setText(_translate("CategoryWindow", "Submit"))
        self.cancel_btn.setText(_translate("CategoryWindow", "Cancel"))

