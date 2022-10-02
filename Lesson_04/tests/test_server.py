import sys
import unittest

from Lesson_04.server import get_server_param


class ServerCLITest(unittest.TestCase):
    @staticmethod
    def get_args(line):
        sys.argv = [""]
        sys.argv.extend([x for x in line.split()])

    def test_cli_server(self):
        self.get_args("")  # пропущены все параметры, по умолчанию "0.0.0.0", 7777
        self.assertEqual(get_server_param(), ("0.0.0.0", 7777))

        self.get_args("-a8.8.8.8")  # пропущены 2-й параметр
        self.assertEqual(get_server_param(), ("8.8.8.8", 7777))

        self.get_args("-p8080")  # пропущен 1-й параметр
        self.assertEqual(get_server_param(), ("0.0.0.0", 8080))

        self.get_args("--addr 255.255.255.255 --port 7890")  # мах значение
        self.assertEqual(get_server_param(), ("255.255.255.255", 7890))

        self.get_args("--addr 256.256.256.256")  # превышены значения в ip адресе
        with self.assertRaises(SystemExit) as cm:
            get_server_param()
        self.assertGreater(cm.exception.code, 0)

        self.get_args("--addr address  --port 9999")  # address не в виде xxx.xxx.xxx.xxx
        with self.assertRaises(SystemExit) as cm:
            get_server_param()
        self.assertGreater(cm.exception.code, 0)

        self.get_args("--addr 0.0.0.0  --port port")  # port не число
        with self.assertRaises(SystemExit) as cm:
            get_server_param()
        self.assertGreater(cm.exception.code, 0)


if __name__ == "__main__":
    unittest.main()
