import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class SlowSearcherThread(qtc.QThread):
    """A somewhat deliberately slow searcher."""

    match_found = qtc.pyqtSignal(str)
    directory_changed = qtc.pyqtSignal(str)
    finished = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.term = None

    @qtc.pyqtSlot(str)
    def set_term(self, term):
        self.term = term

    @qtc.pyqtSlot()
    def run(self):
        #print(f'Beginning search for: {self.term}')
        root = qtc.QDir.rootPath()
        self._search(self.term, root)
        self.finished.emit()

    def _search(self, term, path):
        self.directory_changed.emit(path)
        directory = qtc.QDir(path)
        directory.setFilter(
            directory.filter() |
            qtc.QDir.NoDotAndDotDot |
            qtc.QDir.NoSymLinks
        )
        for entry in directory.entryInfoList():
            if term in entry.filePath():
                print(entry.filePath())
                self.match_found.emit(entry.filePath())
            if entry.isDir():
                self._search(term, entry.filePath())


class SearchForm(qtw.QWidget):

    textChanged = qtc.pyqtSignal(str)
    returnPressed = qtc.pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QVBoxLayout())
        self.search_term_inp = qtw.QLineEdit(
            placeholderText='Search Term',
            textChanged=self.textChanged,
            returnPressed=self.returnPressed)
        self.layout().addWidget(self.search_term_inp)
        self.results = qtw.QListWidget()
        self.layout().addWidget(self.results)
        self.returnPressed.connect(self.results.clear)

    def addResult(self, result):
        self.results.addItem(result)



class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here

        form = SearchForm()
        self.setCentralWidget(form)
        self.ss = SlowSearcherThread()

        # Connect to search engine
        form.textChanged.connect(self.ss.set_term)
        form.returnPressed.connect(self.ss.start)
        self.ss.match_found.connect(form.addResult)
        self.ss.finished.connect(self.on_finished)
        self.ss.directory_changed.connect(self.on_directory_changed)

        # End main UI code
        self.show()

    def on_finished(self):
        self.statusBar().showMessage('Search Finished')

    def on_directory_changed(self, path):
        self.statusBar().showMessage(f'Searching in: {path}')


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
