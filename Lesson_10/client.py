import json
import queue
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from api import Member


class Client:
    def __init__(self, address='localhost', port=10000):
        self.address = (address, port)
        self.user_msg_queue = queue.Queue()
        self.server_msg_queue = queue.Queue()
        self.member = Member(input("Input nickname: >"))  # NickName, password, room

    def get_server_message(self, sock):  # отдельный поток для приема сообщений с сервера
        while True:
            self.server_msg_queue.put(sock.recv(1024).decode('utf-8'))

    def get_user_message(self):  # отдельный поток для клавиатурного ввода
        while True:
            if (s := input()) == 'q':  # выход
                self.user_msg_queue.put(s)
            else:
                self.user_msg_queue.put(self.member.message(s).json())

    def run(self):
        with socket(AF_INET, SOCK_STREAM) as sock:
            sock.connect(self.address)  # Соединиться с сервером

            thr1 = threading.Thread(target=self.get_user_message, daemon=True)
            thr2 = threading.Thread(target=self.get_server_message, args=(sock,), daemon=True)
            thr1.start()
            thr2.start()
            self.user_msg_queue.put(self.member.join().json())  # запрос на присоединение к чату

            while True:
                if self.user_msg_queue.qsize() > 0:
                    str_ = self.user_msg_queue.get()
                    if str_ == 'q':
                        break
                    if str_:  # если не пустая
                        sock.send(str_.encode('utf-8'))  # Отправить на сервер

                if self.server_msg_queue.qsize() > 0:
                    str_ = self.server_msg_queue.get()  # забираем сообщение от сервера из очереди
                    dict_ = json.loads(str_)
                    print('', end='\r')  # в начало строки (печать поверх >)
                    if 'response' in dict_:
                        print(dict_.get("message"))
                    elif dict_.get("action") == 'msg':
                        print(f'{dict_.get("author")}: {dict_.get("message")}')
                    else:
                        print("???: unrecognized message")
                    print('  > ', end='')  # приглашение
                time.sleep(0.01)

            print("End.")


if __name__ == '__main__':
    Client().run()
