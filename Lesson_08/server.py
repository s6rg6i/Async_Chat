import time

import select
from socket import socket, AF_INET, SOCK_STREAM
import json

CHAT_FILE = 'chat.txt'
address = ('', 10000)


def rsp_welcome(msg, dict_):
    out = [(1, f'{{"response": 200, "message": "{dict_.get("room")}: Welcome to our chat room!"}}')]
    with open(CHAT_FILE, encoding="utf-8") as f:  # считываем сообщения чата
        lines = f.readlines()
    out = [*out, *[(1, line) for line in lines[-25:]]]  # последние 25 сообщений для передачи
    return out


def rsp_message(msg, dict_):
    with open(CHAT_FILE, 'a', encoding='utf-8') as f:
        print(msg, file=f)
    return [(0, msg), ]


def rsp_leave(msg, dict_):
    return [(1, '{"response": 200, "alert": "By!"}'), ]


def unknown_action(msg, dict_):
    return [(1, f'{{"response": 404, "message": "Unknown message: {msg}"}}')]


def parse_message(msg: str):
    """ Разбираем полученное сообщение и вызываем соответствующую функцию"""
    functions = {"join": rsp_welcome, "msg": rsp_message, "leave": rsp_leave}
    try:
        dict_ = json.loads(msg)
    except json.JSONDecodeError:
        dict_ = {}
    return functions.get(dict_.get("action"), unknown_action)(msg, dict_)


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


def write_responses(requests, w_clients, all_clients):
    """ Ответ сервера клиентам, от которых были запросы """
    resp = ''
    for sock in w_clients:
        if sock in requests:
            resp = requests[sock]

    for sock in all_clients:
        l_resp = parse_message(resp)
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


def server():
    clients = []
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    print(f"Running server on {address}")
    sock.listen(5)
    sock.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = sock.accept()  # Проверка подключений
        except OSError:
            pass  # timeout вышел
        else:
            print("Получен запрос на соединение от %s" % str(addr))
            clients.append(conn)
        finally:
            # Проверить наличие событий ввода-вывода
            wait = 10
            r, w = [], []
            try:
                r, w, e = select.select(clients, clients, [], wait)
            except OSError:
                pass  # Ничего не делать, если какой-то клиент отключился
            requests = read_requests(r, clients)  # Сохраним запросы клиентов
            if requests:
                write_responses(requests, w, clients)  # Выполним отправку ответов клиентам


if __name__ == "__main__":
    server()
    # s = '{"action": "join", "time": 1665998251.5553887, "room": "my chat"}'
    # print(parse_message(s))
    # s1 = '{"action": "msg", "time": 1665998251.5553887, "to": "my chat", "author": "user1", "message": "Привет!!!"}'
    # print(parse_message(s1))
