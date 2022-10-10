import socket
from json import loads, dumps
import logging
from log import server_log_config

module = logging.getLogger('server')


def response_presence(message):
    if message.get("action", "") == "presence" and "time" in message and "user" in message:
        return dict(response=200)  # OK
    return dict(response=400)


def socket_server(host="0.0.0.0", port=7890):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_sock:
        server_sock.bind((host, port))
        module.debug(f"Running socket server on {host}:{port}")
        server_sock.listen(5)

        while True:
            client, addr = server_sock.accept()
            with client:
                message = loads(client.recv(1000).decode("ascii"))  # Форм.JSON из принятого сообщения (1000:р-р буфера)
                module.debug(f"Server received:\n{dumps(message, indent=4, sort_keys=True)}")
                if message.get("action", "") == "exit":
                    answer = dict(response=200)
                    module.debug(f"Server sends:\n{dumps(answer, indent=4, sort_keys=True)}")
                    client.send(dumps(answer).encode("ascii"))
                    break
                answer = response_presence(message)  # валидация и формирование JSON ответа
                module.debug(f"Server sends:\n{dumps(answer, indent=4, sort_keys=True)}")
                client.send(dumps(answer).encode("ascii"))  # Преобразование JSON в Bytes и отправка ответа


if __name__ == "__main__":
    socket_server()
