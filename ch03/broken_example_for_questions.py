import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc

class TimeForm(qtw.QWidget):

    submitted = qtc.pyqtSignal(qtc.QTime)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QHBoxLayout())
        self.time_inp = qtw.QTimeEdit(self)
        #self.time_inp = qtw.QTimeEdit(self, objectName='time_inp')
        self.layout().addWidget(self.time_inp)
        #qtc.QMetaObject.connectSlotsByName(self)

    def on_time_inp_editingFinished(self):
        self.submitted.emit(self.time_inp.time())
        self.destroy()

class MainWindow(qtw.QWidget):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        self.tf = TimeForm()
        self.tf.show()

        self.tf.submitted.connect(lambda x: print(x))

        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
