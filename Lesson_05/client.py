import logging
from time import time, ctime
from socket import AF_INET, SOCK_STREAM, socket
from json import loads, dumps
from log import client_log_config

module = logging.getLogger('client')


def validate_port(x):  # проверка на число и границы [0:65535]
    try:
        if 0 < int(x) < 2 ** 16:
            return True
        else:
            raise ValueError
    except ValueError:
        module.error("Wrong <port>: should be a number between 0 and 65535")
        return False


def validate_addr(x):  # проверка формата 'x.x.x.x', где x число [0:255] или localhost
    try:
        if x == 'localhost':
            return True
        val = [n for n in map(int, x.split('.')) if 0 <= n < 256]
        if len(val) == 4:
            return True
        else:
            raise ValueError
    except (ValueError, AttributeError):
        module.error("Wrong <host>: should be written in a form of dot-decimal notation (each number < 256)")
        return False


def jim_presence(account_name="guest"):
    return dict(
        action="presence", time=ctime(time()), type="status", user=dict(account_name=account_name, status="online")
    )


def jim_exit_server():  # команда на завершение работы сервера
    return dict(action="exit")


def socket_client(jim, host="localhost", port=7890):
    if not all((validate_addr(host), validate_port(port))):
        module.error(f"Fatal Error: wrong socket")
        exit(3)
    with socket(AF_INET, SOCK_STREAM) as client_sock:
        try:
            client_sock.connect((host, port))
            message = jim()  # Формируем <presence> сообщение
            module.debug(f"Client sends:\n{dumps(message, indent=4, sort_keys=True)}")
            client_sock.send(dumps(message).encode("ascii"))  # Отправляем <presence> сообщение на сервер
            answer = loads(client_sock.recv(1000).decode("ascii"))  # Получаем ответ
            module.debug(f"Client received:\n{dumps(answer, indent=4, sort_keys=True)}")
        except ConnectionRefusedError as e:
            module.error(f"Fatal Error: {e}")
            exit(4)
    return answer


if __name__ == "__main__":
    socket_client(jim_presence)
    socket_client(jim_exit_server)
