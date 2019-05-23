import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from PyQt5 import QtMultimedia as qtmm

import resources


class SoundButton(qtw.QPushButton):

    def __init__(self, wav_file, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wav_file = wav_file
        self.player = qtmm.QSoundEffect()
        self.player.setSource(qtc.QUrl.fromLocalFile(wav_file))
        self.clicked.connect(self.player.play)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        dialpad = qtw.QWidget()
        self.setCentralWidget(dialpad)
        dialpad.setLayout(qtw.QGridLayout())

        for i, symbol in enumerate('123456789*0#'):
            button = SoundButton(f':/dtmf/{symbol}.wav', symbol)
            row = i // 3
            column = i % 3
            dialpad.layout().addWidget(button, row, column)

        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
