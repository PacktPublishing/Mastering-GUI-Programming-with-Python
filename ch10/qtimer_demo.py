import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class AutoCloseDialog(qtw.QDialog):

    def __init__(self, parent, title, message, timeout):
        super().__init__(parent)
        self.setModal(False)
        self.setWindowTitle(title)
        self.setLayout(qtw.QVBoxLayout())
        self.layout().addWidget(qtw.QLabel(message))
        self.timeout = timeout

    def show(self):
        super().show()
        # Wrong:
        #from time import sleep
        #sleep(self.timeout)
        #self.hide()
        # Right:
        qtc.QTimer.singleShot(self.timeout * 1000, self.hide)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        # Using a singleshot timer
        self.dialog = AutoCloseDialog(
            self,
            "Self-destructing message",
            "This message will self-destruct in 10 seconds",
            10
        )
        self.dialog.show()


        # Using an interval timer
        interval_seconds = 10
        self.timer = qtc.QTimer()
        self.timer.setInterval(interval_seconds * 1000)

        self.interval_dialog = AutoCloseDialog(
            self, "It's time again",
            f"It has been {interval_seconds} seconds "
            "since this dialog was last shown.", 2000)
        self.timer.timeout.connect(self.interval_dialog.show)
        self.timer.start()
        toolbar = self.addToolBar('Tools')
        toolbar.addAction('Stop Bugging Me', self.timer.stop)
        toolbar.addAction('Start Bugging Me', self.timer.start)

        # Getting data from a timer
        self.timer2 = qtc.QTimer()
        self.timer2.setInterval(1000)
        self.timer2.timeout.connect(self.update_status)
        self.timer2.start()
        #self.show()
        #return

        # Does a blocking call in a timer block the UI?

        # create timer
        #qtc.QTimer.singleShot(1, self.long_blocking_callback)
        # Yes, yes it does.

        # End main UI code

        self.show()

    def update_status(self):
        if self.timer.isActive():
            time_left = (self.timer.remainingTime() // 1000) + 1
            self.statusBar().showMessage(
                f"Next dialog will be shown in {time_left} seconds.")
        else:
            self.statusBar().showMessage('Dialogs are off.')

    def long_blocking_callback(self):
        from time import sleep
        self.statusBar().showMessage('Beginning a long blocking function.')
        sleep(30)
        self.statusBar().showMessage('Ending a long blocking function.')

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
