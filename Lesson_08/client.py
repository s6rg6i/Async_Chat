import json
import queue
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM

from api import Member, Message

user_msg_queue, server_msg_queue = queue.Queue(), queue.Queue()
address = ('localhost', 10000)
member = Member(input("Input nickname:"))  # NickName, password, room


def get_user_message(inp_queue):  # отдельный поток, чтобы клавиатурный ввод не блокировал основной
    while True:
        if (s := input()) == 'q':  # выход
            user_msg_queue.put(s)
        else:
            user_msg_queue.put(member.message(s).json())


def get_server_message(sock, sock_queue):  # отдельный поток, чтобы ожидание сообщений с сервера не блокировал основной
    while True:
        server_msg_queue.put(sock.recv(1024).decode('utf-8'))


def client():
    with socket(AF_INET, SOCK_STREAM) as sock:
        sock.connect(address)  # Соединиться с сервером

        user_msg_thread = threading.Thread(target=get_user_message, args=(user_msg_queue,), daemon=True)
        server_msg_thread = threading.Thread(target=get_server_message, args=(sock, server_msg_queue,), daemon=True)
        user_msg_thread.start()
        server_msg_thread.start()
        user_msg_queue.put(member.join().json())  # запрос на присоединение к чату

        while True:
            if user_msg_queue.qsize() > 0:
                str_ = user_msg_queue.get()
                if str_ == 'q':
                    break
                if str_:  # если не пустая
                    sock.send(str_.encode('utf-8'))  # Отправить на сервер

            if server_msg_queue.qsize() > 0:
                str_ = server_msg_queue.get()  # забираем сообщение от сервера из очереди
                dict_ = json.loads(str_)
                print('', end='\r')  # в начало строки (печать поверх >)
                if 'response' in dict_:
                    print(dict_.get("message"))
                elif dict_.get("action") == 'msg':
                    print(f'{dict_.get("author")}: {dict_.get("message")}')
                else:
                    print("???: unrecognized message")
                print('>', end='')  # приглашение
            time.sleep(0.01)

        print("End.")


if __name__ == '__main__':
    client()
