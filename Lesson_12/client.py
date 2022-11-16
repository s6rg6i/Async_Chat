import json
import queue
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from jim_api import Jim


class SocketClient:
    def __init__(self, address='localhost', port=10000):
        self.address = (address, port)
        self.user_msg_queue = queue.Queue()
        self.server_msg_queue = queue.Queue()
        self.member = Jim(input("Input nickname: >"))  # NickName, password, room
        self.command_query = {
            'q': lambda _: exit(0),
            '$$join': lambda _: self.member.join(),  # присоединиться к чату
            '$$leave': lambda _: self.member.leave(),  # покинуть чат
            '$$get_contacts': lambda _: self.member.get_contacts(),  # получить список пользователей чата
            '$$get_messages': lambda _: self.member.get_messages(),  # получить последние сообщения чата
            '$$add_contact': lambda name: self.member.add_contact(name),  # добавить контакт в чата
            '$$del_contact': lambda name: self.member.del_contact(name),  # удалить контакт из чата
        }

    def kbd_message_parser(self, message: str) -> str:
        return self.command_query.get(message, self.member.message)(message)

    @staticmethod
    def srv_message_parser(dict_: dict) -> str:
        if dict_.get('action', '') == 'msg':
            return f'{dict_.get("author", "")}: {dict_.get("message", "")}'
        if rsp := dict_.get('response', 0):
            if rsp == 298:  # список пользователей
                return '\n'.join([i for i in dict_.get('user_list', [])])
            return dict_.get('error', '') if rsp >= 400 else dict_.get('alert', '')
        else:
            return "???: unrecognized server message"

    def get_server_message(self, sock):  # отдельный поток для приема сообщений с сервера
        while True:
            self.server_msg_queue.put(sock.recv(1024).decode('utf-8'))

    def get_user_message(self):  # отдельный поток для клавиатурного ввода
        while True:
            self.user_msg_queue.put(input())  # $$... команда, иначе сообщение для отправки

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(self.address)  # Соединиться с сервером

            thr1 = threading.Thread(target=self.get_user_message, daemon=True)
            thr2 = threading.Thread(target=self.get_server_message, args=(sock,), daemon=True)
            thr1.start()
            thr2.start()
            self.user_msg_queue.put('$$join')  # запрос на присоединение к чату

            while True:
                if self.user_msg_queue.qsize():
                    if str_ := self.user_msg_queue.get():  # если строка не пустая
                        str_ = scl.kbd_message_parser(str_)
                        sock.send(str_.encode('utf-8'))  # Отправить на сервер

                if self.server_msg_queue.qsize():
                    print('', end='\r')  # в начало строки (печать поверх >)
                    print(self.srv_message_parser(json.loads(self.server_msg_queue.get())))  # строка для вывода
                    print('  > ', end='')  # приглашение
                time.sleep(0.001)


if __name__ == '__main__':
    scl = SocketClient()
    scl.run()

    # for _ in range(5):  # проверка kbd_message_parser
    #     s = input()
    #     sss = scl.kbd_message_parser(s)
    #     print(sss)
