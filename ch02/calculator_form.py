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
        lcd = qtw.QLCDNumber(self)
        self.layout().addWidget(lcd)

        history = qtw.QLineEdit(self, placeholderText='History')
        self.layout().addWidget(history)

        button_texts = [
            'Clear', 'BackSpace', 'Mem', 'Mem Clear',
            '1', '2', '3', '+',
            '4', '5', '6', '-',
            '7', '8', '9', '×',
            '.', '0', '=', '÷'
        ]
        button_layout = qtw.QGridLayout()
        self.layout().addLayout(button_layout)
        buttons = []
        for num, button_text in enumerate(button_texts):
            button = qtw.QPushButton(button_text, self)
            button.setSizePolicy(qtw.QSizePolicy.Expanding, qtw.QSizePolicy.Expanding)
            buttons.append(button)
            row = num // 4
            column = num % 4
            button_layout.addWidget(button, row, column)
        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
