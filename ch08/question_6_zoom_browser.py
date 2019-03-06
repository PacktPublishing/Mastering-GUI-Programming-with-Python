import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtWebEngineWidgets as qtwe


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor."""
        super().__init__()
        # Main UI code goes here
        # navigation toolbar
        navigation = self.addToolBar('Navigation')
        style = self.style()
        self.back = navigation.addAction('Back')
        self.back.setIcon(style.standardIcon(style.SP_ArrowBack))
        self.forward = navigation.addAction('Forward')
        self.forward.setIcon(style.standardIcon(style.SP_ArrowForward))
        self.reload = navigation.addAction('Reload')
        self.reload.setIcon(style.standardIcon(style.SP_BrowserReload))
        self.stop = navigation.addAction('Stop')
        self.stop.setIcon(style.standardIcon(style.SP_BrowserStop))
        self.urlbar = qtw.QLineEdit()
        navigation.addWidget(self.urlbar)
        self.go = navigation.addAction('Go')
        self.go.setIcon(style.standardIcon(style.SP_DialogOkButton))

        # single browser view
        #webview = qtwe.QWebEngineView()
        #self.setCentralWidget(webview)
        #self.go.triggered.connect(lambda: webview.load(
        #    qtc.QUrl(self.urlbar.text())))
        #self.back.triggered.connect(webview.back)
        #self.forward.triggered.connect(webview.forward)
        #self.reload.triggered.connect(webview.reload)
        #self.stop.triggered.connect(webview.stop)

        # browser tabs
        self.tabs = qtw.QTabWidget(
            tabsClosable=True, movable=True)
        self.tabs.tabCloseRequested.connect(self.tabs.removeTab)
        self.new = qtw.QPushButton('New')
        self.tabs.setCornerWidget(self.new)
        self.setCentralWidget(self.tabs)

        self.back.triggered.connect(self.on_back)
        self.forward.triggered.connect(self.on_forward)
        self.reload.triggered.connect(self.on_reload)
        self.stop.triggered.connect(self.on_stop)
        self.go.triggered.connect(self.on_go)
        self.urlbar.returnPressed.connect(self.on_go)
        self.new.clicked.connect(self.add_tab)

        # Profile sharing
        self.profile = qtwe.QWebEngineProfile()

        # History
        history_dock = qtw.QDockWidget('History')
        self.addDockWidget(qtc.Qt.RightDockWidgetArea, history_dock)
        self.history_list = qtw.QListWidget()
        history_dock.setWidget(self.history_list)
        self.tabs.currentChanged.connect(self.update_history)
        self.history_list.itemDoubleClicked.connect(self.navigate_history)

        # Altering Settings
        settings = qtwe.QWebEngineSettings.defaultSettings()
        settings.setFontFamily(
            qtwe.QWebEngineSettings.SansSerifFont, 'Impact')
        settings.setAttribute(
            qtwe.QWebEngineSettings.PluginsEnabled, True)

        # Zoom controls
        navigation.addAction('Zoom In', self.zoom_in)
        navigation.addAction('Zoom Out', self.zoom_out)

        self.add_tab()
        # End main UI code
        self.show()


    ################
    # Zoom Methods #
    ################
    def zoom_in(self):
        webview = self.tabs.currentWidget()
        webview.setZoomFactor(webview.zoomFactor() * 1.1)

    def zoom_out(self):
        webview = self.tabs.currentWidget()
        webview.setZoomFactor(webview.zoomFactor() * .9)


    ##########################
    # Browser Tabs Functions #
    ##########################

    def add_tab(self, *args):
        webview = qtwe.QWebEngineView()
        tab_index = self.tabs.addTab(webview, 'New Tab')

        webview.urlChanged.connect(
            lambda x: self.tabs.setTabText(tab_index, x.toString()))
        webview.urlChanged.connect(
            lambda x: self.urlbar.setText(x.toString()))

        # make it so pop-up windows call this method
        webview.createWindow = self.add_tab

        # History
        webview.urlChanged.connect(self.update_history)

        # Profile
        page = qtwe.QWebEnginePage(self.profile)
        webview.setPage(page)

        # set default content
        webview.setHtml(
            '<h1>Blank Tab</h1><p>It is a blank tab!</p>',
            qtc.QUrl('about:blank'))

        return webview

    def on_back(self):
        self.tabs.currentWidget().back()

    def on_forward(self):
        self.tabs.currentWidget().forward()

    def on_reload(self):
        self.tabs.currentWidget().reload()

    def on_stop(self):
        self.tabs.currentWidget().stop()

    def on_go(self):
        self.tabs.currentWidget().load(
            qtc.QUrl(self.urlbar.text()))

    ##################
    # History Method #
    ##################

    def update_history(self, *args):
        # show history
        self.history_list.clear()
        webview = self.tabs.currentWidget()
        if webview:
            history = webview.history()
            for history_item in reversed(history.items()):
                list_item = qtw.QListWidgetItem()
                list_item.setData(qtc.Qt.DisplayRole, history_item.url())
                self.history_list.addItem(list_item)

    def navigate_history(self, item):
        qurl = item.data(qtc.Qt.DisplayRole)
        if self.tabs.currentWidget():
            self.tabs.currentWidget().load(qurl)

if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    mw = MainWindow()
    sys.exit(app.exec())
