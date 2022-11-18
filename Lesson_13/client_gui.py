import sys
from socket import socket, AF_INET, SOCK_STREAM

from PyQt5 import QtWidgets, QtCore
from ui.chat_gui import Ui_MainWindow

address = ('localhost', 10000)


class SockRecvMonitor(QtCore.QThread):  # Мониторинг входящих сообщений
    on_recv_data = QtCore.pyqtSignal(str)

    def __init__(self, server_socket, parent=None):
        QtCore.QThread.__init__(self, parent)
        self.server_socket = server_socket
        self.message = None

    def run(self):
        while True:
            self.message = self.server_socket.recv(1024)
            self.on_recv_data.emit(self.message.decode('utf-8'))


class GuiClientApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_btn_state(conn=True, send=False, cont=False)

        self.sock = socket(AF_INET, SOCK_STREAM)
        self.message_monitor = SockRecvMonitor(self.sock)

        self.ui.btn_conn.clicked.connect(self.connect)
        self.ui.btn_cont.clicked.connect(self.add_contact)
        self.ui.btn_send.clicked.connect(self.send_msg)

    def connect(self):
        try:
            self.sock.connect(address)
            self.message_monitor.on_recv_data.connect(self.update_chat)
            self.message_monitor.start()  # Запускаем мониторинг входящих сообщений
            self.set_btn_state(send=True, conn=False, cont=True)
            [self.write_contact(f'Contact_{i:02}') for i in range(5)]
        except OSError:
            self.write('Connecting ERROR!', clear=True)

    def add_contact(self):
        if contact := self.ui.line_cont.text():
            self.ui.text_cont.appendPlainText(contact)
            self.ui.line_cont.clear()

    def send_msg(self):
        if msg := self.read():
            try:
                self.write(f'[Вы]: {msg}')
                self.sock.send(msg.encode('utf-8'))
            except OSError:
                self.sock.close()
                sys.exit()

    def set_btn_state(self, send=True, conn=True, cont=True):
        self.ui.btn_conn.setEnabled(conn)
        self.ui.btn_cont.setEnabled(cont)
        self.ui.btn_send.setEnabled(send)

    def closeEvent(self, event):  # [x] overrides method QWidget. Закрытие окна
        self.sock.close()

    def update_chat(self, value):  # Пришло сообщение от сервера. Обновляем окно чата
        self.write(value)

    def write(self, str_, clear=False):
        if clear:
            self.ui.text_chat.clear()
        self.ui.text_chat.appendPlainText(str_)

    def read(self):
        message = self.ui.line_msg.text()
        self.ui.line_msg.clear()
        return message

    def write_contact(self, str_):
        self.ui.text_cont.appendPlainText(str_)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = GuiClientApp()
    myapp.show()
    sys.exit(app.exec_())
