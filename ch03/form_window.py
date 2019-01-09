import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class FormWindow(qtw.QWidget):

    submitted = qtc.pyqtSignal([str], [int, str])

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        self.edit = qtw.QLineEdit()
        self.submit = qtw.QPushButton('Submit', clicked=self.onSubmit)

        self.layout().addWidget(self.edit)
        self.layout().addWidget(self.submit)

    def onSubmit(self):
        if self.edit.text().isdigit():
            text = self.edit.text()
            self.submitted[int, str].emit(int(text), text)
        else:
            self.submitted[str].emit(self.edit.text())
        self.close()

class MainWindow(qtw.QWidget):

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())

        self.label = qtw.QLabel('Click "change" to change this text.')
        self.change = qtw.QPushButton("Change", clicked=self.onChange)
        self.layout().addWidget(self.label)
        self.layout().addWidget(self.change)
        self.show()

    @qtc.pyqtSlot()
    def onChange(self):
        self.formwindow = FormWindow()
        #self.formwindow.submitted.connect(self.label.setText)
        self.formwindow.submitted[str].connect(self.onSubmittedStr)
        self.formwindow.submitted[int, str].connect(self.onSubmittedIntStr)
        self.formwindow.show()

    @qtc.pyqtSlot(str)
    def onSubmittedStr(self, string):
        self.label.setText(string)

    @qtc.pyqtSlot(int, str)
    def onSubmittedIntStr(self, integer, string):
        text = f'The string {string} becomes the number {integer}'
        self.label.setText(text)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
