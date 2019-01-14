import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg


class InventoryNumberValidator(qtg.QValidator):
    """Validates an inventory number in the format XX-999-9999X

    X is an uppercase letter from A to Z excluding O and I.
    9 is any digit from 0 to 9.
    """

    valid_letters = 'ABCDEFGHJKLMNPQRSTUVWXYZ'
    def validate(self, string, index):
        # one approach is to break the string into segments
        # and test each segment for proper content
        state = qtg.QValidator.Acceptable
        seg1 = string[0:2]
        dash1 = string[2:3]
        seg2 = string[3:6]
        dash2 = string[6:7]
        seg3 = string[7:11]
        seg4 = string[11:12]

        if not all([char in self.valid_letters for char in seg1 + seg4]):
            state = qtg.QValidator.Invalid
        elif not all([char.isdigit() for char in seg2 + seg3]):
            state = qtg.QValidator.Invalid
        elif not all([char == '-' for char in dash1 + dash2]):
            state = qtg.QValidator.Invalid
        elif len(string) > 12:
            state = qtg.QValidator.Invalid
        elif not all([seg1, dash1, seg2, dash2, seg3, seg4]):
            state = qtg.QValidator.Intermediate

        return (state, string, index)


class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        self.setLayout(qtw.QVBoxLayout())
        inventory_number = qtw.QLineEdit()
        inventory_number.setValidator(InventoryNumberValidator())
        self.layout().addWidget(inventory_number)
        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
