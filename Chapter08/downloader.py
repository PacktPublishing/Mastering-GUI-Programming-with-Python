import sys
from os import path
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc


class Downloader(qtc.QObject):

    def __init__(self, url):
        super().__init__()
        self.manager = qtn.QNetworkAccessManager(
            finished=self.on_finished)
        self.request = qtn.QNetworkRequest(qtc.QUrl(url))
        self.manager.get(self.request)

    def on_finished(self, reply):
        filename = reply.url().fileName() or 'download'
        if path.exists(filename):
            print('File already exists, not overwriting.')
            sys.exit(1)
        with open(filename, 'wb') as fh:
            fh.write(reply.readAll())
        print(f"{filename} written")
        sys.exit(0)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <download url>')
        sys.exit(1)
    app = qtc.QCoreApplication(sys.argv)
    d = Downloader(sys.argv[1])
    sys.exit(app.exec_())
