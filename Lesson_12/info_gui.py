from server import ADDRESS, PORT
from storage import DbChat, DB_PATH
from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QVBoxLayout, QPushButton
import sys


class ServerInfoGUI(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.db_chat = DbChat()
        self.setWindowTitle("Information")
        self.resize(600, 800)

        self.text_edit = QTextEdit()
        self.button1 = QPushButton("Clients")
        self.button2 = QPushButton("Statistics")
        self.button3 = QPushButton("Configuration")

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        self.setLayout(layout)

        self.button1.clicked.connect(self.button1_clicked)
        self.button2.clicked.connect(self.button2_clicked)
        self.button3.clicked.connect(self.button3_clicked)

    def button1_clicked(self):
        self.text_edit.setPlainText('\n'.join(self.db_chat.list_of_users()))

    def button2_clicked(self):
        self.text_edit.setPlainText('Statistics on clients')
        for k, val in self.db_chat.statistics_by_clients_all().items():
            self.text_edit.append(f"     {k[0]} {k[1]}")
            for id_, date_, ip_ in val:
                self.text_edit.append(f"{ip_:20} {date_}")

    def button3_clicked(self):
        self.text_edit.setPlainText('Server configuration')  # подключение к БД, идентификация
        self.text_edit.append(f'DataBase Path:\n{DB_PATH}')
        self.text_edit.append(f'Server run on "{ADDRESS}":{PORT}')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    windows = ServerInfoGUI()
    windows.show()
    sys.exit(app.exec_())
