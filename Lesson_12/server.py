import time
from queue import Queue
from socket import socket, AF_INET, SOCK_STREAM
import select
import json

from storage import DbChat
from jim_api import Jim

# Сокет
ADDRESS = ''
PORT = 10000
BLOCK_LEN = 4096


class MessageParser:
    def __init__(self, db_chat):
        self.db_chat: DbChat = db_chat
        self.jim_dict = {}
        self.jim_str = ''
        self.functions = {"join": self.welcome_proc, "msg": self.message_proc, "leave": self.leave_proc,
                          "get_contacts": self.get_contacts, 'get_messages': self.get_messages,
                          'add_contact': self.add_contact, 'del_contact': self.del_contact, }

    def get_messages(self):
        return [1, [*self.db_chat.last_entries()]]

    def get_contacts(self):
        return [1, [Jim.user_list(self.db_chat.list_of_users()), ]]

    def add_contact(self):
        self.db_chat.add_contact(login=self.jim_dict.get('user_id'))
        return [1, [Jim.response_ok('Contact added to the chat room!'), ]]

    def del_contact(self):
        self.db_chat.del_contact(login=self.jim_dict.get('user_id'))
        return [1, [Jim.response_ok('Contact added to the chat room!'), ]]

    @staticmethod
    def welcome_proc():
        return [1, [Jim.response_ok('Welcome to the chat room!')]]

    def message_proc(self):
        self.db_chat.insert_message(self.jim_str)
        return [0, [self.jim_str, ]]

    @staticmethod
    def leave_proc():
        return [1, [Jim.response_ok('By!'), ]]

    @staticmethod
    def error_proc():
        return [1, [Jim.response_err(400, 'Incorrect message'), ]]

    def parse_message(self, message: str):  #
        """ Разбор полученного сообщения и вызов соответствующей функции для формирования ответа.
        :param message: JIM строка, полученная от клиента
        :return: структура [0 | 1, [JIM-строка ответа сервера, JIM-строка, JIM-строка, ...]
                            0-широковещательное сообщение, 1-ответ клиенту
        """
        self.jim_str = message
        try:
            self.jim_dict = json.loads(message)
        except json.JSONDecodeError:
            self.jim_dict = {}
        return self.functions.get(self.jim_dict.get("action"), self.error_proc)()


class Server:
    def __init__(self, address='', port=10000):
        self.address = (address, port)
        self.db_chat = DbChat()
        self.msg_parser = MessageParser(self.db_chat)

    def send_response(self, data: str, sock: socket, all_clients: list):
        """ Ответ сервера клиенту, от которого получено сообщение (клиентам - широковещательно)"""
        type_sending, messages = self.msg_parser.parse_message(data)
        sockets = [sock] if type_sending else all_clients[1:]  # 0 - всем; 1 - клиенту
        for next_sock in sockets:
            for next_msg in messages:
                try:
                    next_sock.sendall(next_msg.encode('utf-8'))  # Ответ клиенту
                    time.sleep(0.001)  # В клиенте такая же задержка (иначе все сообщения идут одним пакетом)
                except OSError:  # Сокет недоступен, клиент отключился
                    self.close_connection(sock, all_clients)

    @staticmethod
    def close_connection(del_socket, socks_list):
        if del_socket in socks_list:
            print(f'Client [{del_socket.fileno()}, {del_socket.getpeername()}] disconnected')
            socks_list.remove(del_socket)  # удаляем из списка на прослушивание
            del_socket.close()  # Закрываем соединение

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as server_socket:
            server_socket.setblocking(False)  # устанавливаем неблокирующий режим серверного сокета
            server_socket.bind(self.address)  # привязываем сокет к адресу
            server_socket.listen()  # переводим сервер для приема подключений
            sockets_list = [server_socket]  # список подключенных сокетов
            message_queues = Queue()  # входная очередь сообщений (socket, message)
            print(f"Running server on {server_socket.fileno()}: '{server_socket}'")

            while sockets_list:
                r, _, e = select.select(sockets_list, [], sockets_list)  # Проверяем наличие событий ввода
                print(f"r:{[i.fileno() for i in r]}")
                for sock in r:  # Перебираем сокеты на прослушивание
                    if sock is server_socket:  # Регистрация нового соединение:
                        new_socket, client_address = sock.accept()  # принять соединение от клиента
                        new_socket.setblocking(False)  # устанавливаем неблокирующий режим нового клиентского сокета
                        sockets_list.append(new_socket)  # добавим новое соединение в список для прослушивания
                        # message_queues[new_socket].put((new_socket,'Привет. Как тебя зовут?'))  # welcome message
                        print(f"Соединение установлено с {client_address}")
                    else:  # Чтение данных
                        if sock in e:
                            self.close_connection(sock, sockets_list)
                            continue
                        try:
                            if data := sock.recv(BLOCK_LEN).decode('utf-8'):
                                message_queues.put((sock, data,))
                            else:
                                self.close_connection(sock, sockets_list)
                        except OSError:
                            self.close_connection(sock, sockets_list)
                while not message_queues.empty():
                    sock, data = message_queues.get_nowait()
                    self.send_response(data, sock, sockets_list)


if __name__ == "__main__":
    Server(ADDRESS, PORT).run()

    # chat = MessageParser()
    # s0 = '{"action": "join", "time": 1665998251.5553887, "room": "my chat"}'
    # s = chat.parse_message(s0)
    # print('\n'.join([f"{x[0]},{x[1]}" for x in s]))
    # s1 = '{"action": "msg", "time": 1665998251.5553887, "to": "my chat", "author": "user1", "message": "Message!!!"}'
    # print(chat.parse_message(s1))
