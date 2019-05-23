import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtNetwork as qtn
from PyQt5 import QtCore as qtc


class TcpChatInterface(qtc.QObject):
    """Network interface for chat messages."""

    port = 7777
    delimiter = '||'
    received = qtc.pyqtSignal(str, str)
    error = qtc.pyqtSignal(str)

    def __init__(self, username, recipient):
        super().__init__()
        self.username = username
        self.recipient = recipient

        self.listener = qtn.QTcpServer()
        self.listener.listen(qtn.QHostAddress.Any, self.port)
        self.listener.newConnection.connect(self.on_connection)
        self.listener.acceptError.connect(self.on_error)
        self.connections = []

        self.client_socket = qtn.QTcpSocket()
        self.client_socket.error.connect(self.on_error)

    def on_connection(self):
        connection = self.listener.nextPendingConnection()
        self.connections.append(connection)
        connection.readyRead.connect(self.process_datastream)

    def process_datastream(self):
        for socket in self.connections:
            self.datastream = qtc.QDataStream(socket)
            if not socket.bytesAvailable():
                continue
            #message_length = self.datastream.readUInt32()
            raw_message = self.datastream.readQString()
            if raw_message and self.delimiter in raw_message:
                username, message = raw_message.split(self.delimiter, 1)
                self.received.emit(username, message)

    def send_message(self, message):
        """Prepare and send a message"""
        raw_message = f'{self.username}{self.delimiter}{message}'
        if self.client_socket.state() != qtn.QAbstractSocket.ConnectedState:
            self.client_socket.connectToHost(self.recipient, self.port)
        self.datastream = qtc.QDataStream(self.client_socket)
        #self.datastream.writeUInt32()
        self.datastream.writeQString(raw_message)

        # Echo locally
        self.received.emit(self.username, message)

    def on_error(self, socket_error):
        # Magic to get the enum name
        error_index = (qtn.QAbstractSocket
                       .staticMetaObject
                       .indexOfEnumerator('SocketError'))
        error = (qtn.QAbstractSocket
                 .staticMetaObject
                 .enumerator(error_index)
                 .valueToKey(socket_error))
        message = f"There was a network error: {error}"
        self.error.emit(message)


class ChatWindow(qtw.QWidget):
    """The form to show and enter chats"""

    submitted = qtc.pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.setLayout(qtw.QGridLayout())
        self.message_view = qtw.QTextEdit(readOnly=True)
        self.layout().addWidget(self.message_view, 1, 1, 1, 2)
        self.message_entry = qtw.QLineEdit(returnPressed=self.send)
        self.layout().addWidget(self.message_entry, 2, 1)
        self.send_btn = qtw.QPushButton('Send', clicked=self.send)
        self.layout().addWidget(self.send_btn, 2, 2)

    def write_message(self, username, message):
        self.message_view.append(f'<b>{username}: </b> {message}<br>')

    def send(self):
        message = self.message_entry.text().strip()
        if message:
            self.submitted.emit(message)
            self.message_entry.clear()


class MainWindow(qtw.QMainWindow):

    def __init__(self):
        """MainWindow constructor.

        Code in this method should define window properties,
        create backend resources, etc.
        """
        super().__init__()
        # Code starts here
        username = qtc.QDir.home().dirName()
        self.cw = ChatWindow()
        self.setCentralWidget(self.cw)
        recipient, _ = qtw.QInputDialog.getText(
            None, 'Recipient',
            'Specify of the IP or hostname of the remote host.')
        if not recipient:
            sys.exit()

        self.interface = TcpChatInterface(username, recipient)
        self.cw.submitted.connect(self.interface.send_message)
        self.interface.received.connect(self.cw.write_message)
        self.interface.error.connect(
            lambda x: qtw.QMessageBox.critical(None, 'Error', x))
        # Code ends here
        self.show()


if __name__ == '__main__':
    app = qtw.QApplication(sys.argv)
    # it's required to save a reference to MainWindow.
    # if it goes out of scope, it will be destroyed.
    mw = MainWindow()
    sys.exit(app.exec())
