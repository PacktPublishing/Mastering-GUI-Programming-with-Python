import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        widgets = [
            qtw.QLabel("I am a label"),
            qtw.QLineEdit(placeholderText="I am a line edit"),
            qtw.QSpinBox(),
            qtw.QCheckBox("I am a checkbox"),
            qtw.QComboBox(editable=True)
        ]
        container = qtw.QWidget()
        self.setCentralWidget(container)
        container.setLayout(qtw.QVBoxLayout())

        for widget in widgets:
            container.layout().addWidget(widget)

        # Style switching combobox
        styles = qtw.QStyleFactory.keys()
        style_combo = qtw.QComboBox()
        style_combo.addItems(styles)
        style_combo.currentTextChanged.connect(self.set_style)
        container.layout().addWidget(style_combo)

        # End main UI code
        self.show()

    def set_style(self, style):
        style = qtw.QStyleFactory.create(style)
        qtw.QApplication.instance().setStyle(style)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
