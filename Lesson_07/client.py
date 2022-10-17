import queue
import threading
import time
from socket import socket, AF_INET, SOCK_STREAM


def read_kbd_input(inp_queue):  # запускаем отдельным потоком, чтобы клавиатурный ввод не блокировал опрос сокета
    while True:
        input_str = input()
        inp_queue.put(input_str)
        if input_str == "q":  # Закрываем поток
            break


def client():
    address = ('localhost', 10000)
    inp_queue = queue.Queue()
    inp_thread = threading.Thread(target=read_kbd_input, args=(inp_queue,), daemon=True)
    inp_thread.start()
    with socket(AF_INET, SOCK_STREAM) as sock:  # Создать сокет TCP
        sock.connect(address)  # Соединиться с сервером
        sock.settimeout(0.5)
        print('Enter the message:')
        while True:
            if inp_queue.qsize() > 0:
                input_str = inp_queue.get()
                # print(f"{input_str=}")
                if input_str == 'q':
                    print("Exit")
                    break
                if input_str:  # если не пустая
                    sock.send(input_str.encode('utf-8'))  # Отправить на сервер
            try:
                s = sock.recv(1024).decode('utf-8')
                print(s)
            except OSError:
                ...
            time.sleep(0.01)

        print("End.")


if __name__ == '__main__':
    client()
