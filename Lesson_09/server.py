from socket import socket, AF_INET, SOCK_STREAM
import time
import select
import json


class MessageParser:
    def __init__(self, char_room='My chat', chat_file='chat.txt'):
        self.char_room = char_room
        self.chat_file = chat_file
        self.json_msg = ''
        self.jim = {}

    def rsp_welcome(self):
        try:
            lines = [(1, line.strip()) for line in open(self.chat_file, encoding="utf-8") if line.strip()]
        except FileNotFoundError:
            lines = []
        out = [(1, f'{{"response": 200, "message": "[{self.jim.get("room")}]: Welcome to our chat room!"}}'), *lines]
        return out

    def rsp_message(self):
        with open(self.chat_file, 'a', encoding='utf-8') as f:
            print(self.json_msg, file=f)
        return [(0, self.json_msg), ]

    def rsp_leave(self):
        return [(1, '{"response": 200, "alert": "By!"}'), ]

    def unknown_action(self):
        return [(1, f'{{"response": 404, "message": "Unknown message: {self.json_msg}"}}')]

    def parse_message(self, message: str):
        """ Разбираем полученное сообщение и вызываем соответствующую функцию"""
        self.json_msg = message
        functions = {"join": self.rsp_welcome, "msg": self.rsp_message, "leave": self.rsp_leave}
        try:
            self.jim = json.loads(self.json_msg)
        except json.JSONDecodeError:
            self.jim = {}
        return functions.get(self.jim.get("action"), self.unknown_action)()


class Server:
    def __init__(self, address='', port=10000):
        self.address = (address, port)
        self.clients = []
        self.sock = socket(AF_INET, SOCK_STREAM)
        self.msg_parser = MessageParser()

    def run(self):
        self.sock.bind(self.address)
        print(f"Running server on {self.address}")
        self.sock.listen(5)
        self.sock.settimeout(0.2)  # Таймаут для операций с сокетом
        while True:
            try:
                conn, addr = self.sock.accept()  # Проверка подключений
            except OSError:
                pass  # timeout вышел
            else:
                print("Получен запрос на соединение от %s" % str(addr))
                self.clients.append(conn)
            finally:
                # Проверить наличие событий ввода-вывода
                r, w = [], []
                try:
                    r, w, e = select.select(self.clients, self.clients, [], 10)
                except OSError:
                    pass  # Ничего не делать, если какой-то клиент отключился
                requests = self.read_requests(r, self.clients)  # Сохраним запросы клиентов
                if requests:
                    self.write_responses(requests, w, self.clients)  # Выполним отправку ответов клиентам

    @staticmethod
    def read_requests(r_clients, all_clients):
        """ Чтение запросов из списка клиентов """
        responses = {}  # Словарь ответов сервера вида {сокет: запрос}
        for sock in r_clients:
            try:
                data = sock.recv(1024).decode('utf-8')
                responses[sock] = data
            except OSError:
                print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                all_clients.remove(sock)
        return responses

    def write_responses(self, requests, w_clients, all_clients):
        """ Ответ сервера клиентам, от которых были запросы """
        resp = ''
        for sock in w_clients:
            if sock in requests:
                resp = requests[sock]

        l_resp = self.msg_parser.parse_message(resp)
        for sock in all_clients:
            for is_only, resp_i in l_resp:
                if sock not in requests and is_only:
                    continue
                try:
                    sock.send(resp_i.encode('utf-8'))  # Эхо-ответ
                    time.sleep(0.01)  # Чтобы все сообщения не шли одним пакетом
                except OSError:  # Сокет недоступен, клиент отключился
                    print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
                    sock.close()
                    all_clients.remove(sock)


if __name__ == "__main__":
    Server().run()

    # chat = MessageParser()
    # s0 = '{"action": "join", "time": 1665998251.5553887, "room": "my chat"}'
    # s = chat.parse_message(s0)
    # print('\n'.join([f"{x[0]},{x[1]}" for x in s]))
    # s1 = '{"action": "msg", "time": 1665998251.5553887, "to": "my chat", "author": "user1", "message": "Message!!!"}'
    # print(chat.parse_message(s1))
