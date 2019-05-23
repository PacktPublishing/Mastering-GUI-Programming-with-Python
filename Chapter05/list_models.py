import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        self.setLayout(qtw.QVBoxLayout())

        data = [
            'Hamburger', 'Cheeseburger',
            'Chicken Nuggets', 'Hot Dog', 'Fish Sandwich'
        ]

        listwidget = qtw.QListWidget()
        listwidget.addItems(data)
        combobox = qtw.QComboBox()
        combobox.addItems(data)
        self.layout().addWidget(listwidget)
        self.layout().addWidget(combobox)

        # make the list widget editable
        for i in range(listwidget.count()):
            item = listwidget.item(i)
            item.setFlags(item.flags() | qtc.Qt.ItemIsEditable)


        # The same, but with a model

        model = qtc.QStringListModel(data)

        listview = qtw.QListView()
        listview.setModel(model)
        model_combobox = qtw.QComboBox()
        model_combobox.setModel(model)

        self.layout().addWidget(listview)
        self.layout().addWidget(model_combobox)

        # End main UI code
        self.show()



if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
