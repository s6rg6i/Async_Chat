from ipaddress import IPv4Address
from time import time, ctime
from socket import AF_INET, SOCK_STREAM, socket
from json import loads, dumps
from argparse import ArgumentParser


def get_client_param(port=7777):
    """параметры командной строки скрипта client.py: <addr> [<port>]
    TCP-порт по умолчанию - 7777;
    примеры: <127.0.0.1 1999>, <localhost>, <-h>"""

    parser = ArgumentParser(description="Socket client")
    parser.add_argument(
        "IP_address",
        type=lambda ip: ip if ip == "localhost" else str(IPv4Address(ip)),
        help="IP address of socket server(is required)",
    )
    parser.add_argument(
        "port",
        type=int,
        help=f"Port of socket server (is not required). Default port is {port}",
        nargs="?",
        default=port,
    )
    args = parser.parse_args()
    return args.IP_address, args.port


def create_presence(account_name="guest"):
    return dict(
        action="presence", time=ctime(time()), type="status", user=dict(account_name=account_name, status="online")
    )


def socket_client():
    host, port = get_client_param(port=7777)

    with socket(AF_INET, SOCK_STREAM) as client_sock:
        client_sock.connect((host, port))
        message = create_presence()  # Формируем <presence> сообщение
        print(f"Отправляется: {message}")
        client_sock.send(dumps(message).encode("ascii"))  # Отправляем <presence> сообщение на сервер
        answer = loads(client_sock.recv(1000).decode("ascii"))  # Получаем ответ
        print(f"Получено: {answer}\nBye!")


if __name__ == "__main__":
    socket_client()
