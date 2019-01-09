import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        # connecting a signal to a slot
        self.quitbutton = qtw.QPushButton('Quit')
        self.quitbutton.clicked.connect(self.close)
        self.layout().addWidget(self.quitbutton)

        # connecting a signal with data to a slot that receives data
        self.entry1 = qtw.QLineEdit()
        self.entry2 = qtw.QLineEdit()
        self.layout().addWidget(self.entry1)
        self.layout().addWidget(self.entry2)
        self.entry1.textChanged.connect(self.entry2.setText)

        # connecting a signal to a python callable
        self.entry2.textChanged.connect(print)

        # Connecting a signal to another signal
        self.entry1.editingFinished.connect(lambda: print('editing finished'))
        self.entry2.returnPressed.connect(self.entry1.editingFinished)

        # This call will fail, because the signals have different argument types
        #self.entry1.textChanged.connect(self.quitbutton.clicked)

        # This won't work, because of signal doesn't send enough args
        self.badbutton = qtw.QPushButton("Bad")
        self.layout().addWidget(self.badbutton)
        self.badbutton.clicked.connect(self.needs_args)

        # This will work, even though the signal sends extra args
        self.goodbutton = qtw.QPushButton("Good")
        self.layout().addWidget(self.goodbutton)
        self.goodbutton.clicked.connect(self.no_args)


        self.show()

    def needs_args(self, arg1, arg2, arg3):
        pass

    def no_args(self):
        print('I need no arguments')

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
