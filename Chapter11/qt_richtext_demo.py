import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI code goes here
        main = qtw.QTextBrowser(minimumWidth=800, minimumHeight=600)
        self.setCentralWidget(main)

        # Must come before the HTML is inserted
        main.document().setDefaultStyleSheet(
            'body {color: #333; font-size: 14px;} '
            'h2 {background: #CCF; color: #443;} '
            'h1 {background: #001133; color: white;} '
        )

        # TextBrowser background is a widget style, not a document style
        main.setStyleSheet('background-color: #EEF;')
        with open('fight_fighter2.html', 'r') as fh:
            main.insertHtml(fh.read())

        main.setOpenExternalLinks(True)

        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
