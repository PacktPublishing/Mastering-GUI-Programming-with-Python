import sys
import json
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5 import QtNetwork as qtn


class Poster(qtc.QObject):

    # emit body of reply
    replyReceived = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.nam = qtn.QNetworkAccessManager()
        self.nam.finished.connect(self.on_reply)

    def make_request(self, url, data, filename):
        print(f"Making request to {url}")
        # Create the request object
        self.request = qtn.QNetworkRequest(url)

        # create the multipart object
        self.multipart = qtn.QHttpMultiPart(qtn.QHttpMultiPart.FormDataType)

        # Write the key-value data to the multipart
        json_string = json.dumps(data)
        http_part = qtn.QHttpPart()
        http_part.setHeader(
            qtn.QNetworkRequest.ContentTypeHeader,
            'text/json'
        )
        http_part.setBody(json_string.encode('utf-8'))
        self.multipart.append(http_part)

        # Write the file data to the multipart
        if filename:
            file_part = qtn.QHttpPart()
            filedata = open(filename, 'rb').read()
            file_part.setHeader(
                qtn.QNetworkRequest.ContentDispositionHeader,
                f'form-data; name="attachment"; filename="{filename}"'
            )
            file_part.setBody(filedata)
            self.multipart.append(file_part)

        # Post the request with the form data
        self.nam.post(self.request, self.multipart)

    def on_reply(self, reply):
        # reply.readAll() returns a QByteArray
        reply_bytes = reply.readAll()
        reply_string = bytes(reply_bytes).decode('utf-8')

        # emit reply
        self.replyReceived.emit(reply_string)



class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        This widget will be our main window.
        We'll define all the UI components in here.
        """
        super().__init__()
        # Main UI code goes here
        widget = qtw.QWidget(minimumWidth=600)
        self.setCentralWidget(widget)
        widget.setLayout(qtw.QVBoxLayout())
        self.url = qtw.QLineEdit()
        self.table = qtw.QTableWidget(columnCount=2, rowCount=5)
        self.table.horizontalHeader().setSectionResizeMode(
            qtw.QHeaderView.Stretch)
        self.table.setHorizontalHeaderLabels(['key', 'value'])
        self.fname = qtw.QPushButton(
            '(No File)', clicked=self.on_file_btn)
        submit = qtw.QPushButton('Submit Post', clicked=self.submit)
        response = qtw.QTextEdit(readOnly=True)
        for w in (self.url, self.table, self.fname, submit, response):
            widget.layout().addWidget(w)

        # Create the poster object
        self.poster = Poster()
        self.poster.replyReceived.connect(self.response.setText)

        # End main UI code
        self.show()

    def on_file_btn(self):
        filename, accepted = qtw.QFileDialog.getOpenFileName()
        if accepted:
            self.fname.setText(filename)

    def submit(self):
        url = qtc.QUrl(self.url.text())
        filename = self.fname.text()
        if filename == '(No File)':
            filename = None
        data = {}
        for rownum in range(self.table.rowCount()):
            key_item = self.table.item(rownum, 0)
            key = key_item.text() if key_item else None
            if key:
                data[key] = self.table.item(rownum, 1).text()
        self.poster.make_request(url, data, filename)


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
