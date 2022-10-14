import select
from socket import socket, AF_INET, SOCK_STREAM


def read_requests(r_clients, all_clients):  # Чтение запросов из списка клиентов

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
    """ Эхо-ответ сервера клиентам, от которых были запросы """
    msg = ''
    for sock in w_clients:
        if sock in requests:
            msg = f"{sock.getpeername()}: {requests[sock]}"

    for sock in all_clients:
        try:
            # resp = requests[sock].encode('utf-8')  # Подготовить и отправить ответ сервера
            sock.send(msg.encode('utf-8'))  # Эхо-ответ сделаем чуть непохожим на оригинал
        except OSError:  # Сокет недоступен, клиент отключился
            print(f'Клиент {sock.fileno()} {sock.getpeername()} отключился')
            sock.close()
            all_clients.remove(sock)


def server():
    address = ('', 10000)
    clients = []
    s = socket(AF_INET, SOCK_STREAM)
    s.bind(address)
    s.listen(5)
    s.settimeout(0.2)  # Таймаут для операций с сокетом
    while True:
        try:
            conn, addr = s.accept()  # Проверка подключений
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
