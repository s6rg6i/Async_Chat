import sys
import unittest
from threading import Thread

from Lesson_04.client import socket_client, jim_exit_server
from Lesson_04.server import socket_server


class TestSocket(unittest.TestCase):
    def setUp(self) -> None:
        sys.argv = [""]  # параметры по умолчанию <0.0.0.0:7777>
        self.thread = Thread(target=socket_server)
        self.thread.start()  # запускаем сервер для тестов

    def tearDown(self) -> None:
        if self.thread:
            sys.argv = ["", "localhost"]
            socket_client(jim=jim_exit_server)  # команда на завершение работы сервера

    def test_0(self):  # Корректное <presence> сообщение
        sys.argv = ["", "localhost"]
        self.assertEqual(socket_client(), {"response": 200})

    def test_1(self):  # клиенту отказано в доступе (разные порты с сервером)
        sys.argv = ["", "localhost", "8000"]
        with self.assertRaises(ConnectionRefusedError) as cm:
            socket_client()
        self.assertEqual(cm.exception.errno, 10061)

    def test_2(self):  # Некорректное <presence> сообщение
        sys.argv = ["", "localhost"]
        f = lambda: dict(action="presence", type="status", user=dict(account_name="user", status="online"))
        self.assertEqual(socket_client(jim=f), {"response": 400})


if __name__ == "__main__":
    unittest.main()
