import sys
from PyQt5 import QtCore as qtc
from PyQt5 import QtNetwork as qtn

class Server(qtn.QTcpServer):

    def __init__(self):
        super().__init__()
        self.newConnection.connect(self.on_new_connection)
        self.connections = []
        self.listen(qtn.QHostAddress.Any, 8080)

    def on_new_connection(self):
        while self.hasPendingConnections():
            cx = self.nextPendingConnection()
            self.connections.append(cx)
            cx.readyRead.connect(self.process_datastream)

    def process_datastream(self):
        for cx in self.connections:
            self.datastream = qtc.QDataStream(cx)
            print(self.datastream.readRawData(cx.bytesAvailable()))
            self.datastream.writeRawData(b'PyQt5 Rocks!')
            cx.disconnectFromHost()

if __name__ == '__main__':
    app = qtc.QCoreApplication(sys.argv)
    server = Server()
    sys.exit(app.exec())
