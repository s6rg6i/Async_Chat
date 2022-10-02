from ipaddress import IPv4Address
import socket
from argparse import ArgumentParser
from json import loads, dumps


def get_server_param(host="0.0.0.0", port=7777):
    """параметры командной строки скрипта server.py: -a --addr <addr> -p --port <port>
    TCP-порт по умолчанию - 7777; IP-адрес по умолчанию - 0.0.0.0;
    примеры: <>, <-p 8888> <--addr 127.0.0.1 --port 1999>, <--addr localhost>, <-h>"""

    parser = ArgumentParser(description="Socket server")
    parser.add_argument(
        "-a",
        "--addr",
        type=lambda ip: ip if ip == "localhost" else str(IPv4Address(ip)),
        help=f"Server IP address. Default: {host}",
        default=host,
    )
    parser.add_argument("-p", "--port", type=int, help=f"Server port. Default: {port}", default=port)
    args = parser.parse_args()
    return args.addr, args.port


def response_presence(message):
    if message.get("action", "") == "presence" and "time" in message and "user" in message:
        return dict(response=200)  # OK
    return dict(response=400)


def socket_server():
    host, port = get_server_param()  # из аргументов командной строки
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        print(f"Running server on {host}:{port}")
        server_sock.listen(5)

        while True:
            client, addr = server_sock.accept()
            with client:
                message = loads(client.recv(1000).decode("ascii"))  # Форм.JSON из принятого сообщения (1000:р-р буфера)
                print(f"Server received: {message}")
                if message.get("action", "") == "exit":
                    client.send(dumps(dict(response=200)).encode("ascii"))
                    break
                answer = response_presence(message)  # валидация и формирование JSON ответа
                print(f"Server sends: {answer}")
                client.send(dumps(answer).encode("ascii"))  # Преобразование JSON в Bytes и отправка ответа


if __name__ == "__main__":
    socket_server()
