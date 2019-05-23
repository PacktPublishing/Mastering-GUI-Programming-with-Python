import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtWebEngineWidgets as qtwe


class WebView(qtwe.QWebEngineView):

    def __init__(self):
        super().__init__()
        script = qtwe.QWebEngineScript()
        script.setSourceCode(
            'function object(){ return {a: 1, b: 2}; }\n'
            'function string(){ return "Test String";}\n'
            'function array() { return ["a", 7, {a: 2}];}\n'
        )
        script.setWorldId(qtwe.QWebEngineScript.MainWorld)
        self.page().scripts().insert(script)
        self.loadFinished.connect(self.on_load)

    def on_load(self, ok):
        self.page().runJavaScript('object()', print)
        self.page().runJavaScript('string()', print)
        self.page().runJavaScript('array()', print)


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI code goes here
        wv = WebView()
        self.setCentralWidget(wv)
        wv.load(qtc.QUrl('about:blank'))
        # End main UI code
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
