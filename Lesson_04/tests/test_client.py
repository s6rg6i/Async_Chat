import sys
import unittest

from Lesson_04.client import get_client_param


class ClintCLITest(unittest.TestCase):
    @staticmethod
    def get_args(line):
        sys.argv = [""]
        sys.argv.extend([x for x in line.split()])

    def test_cli_client(self):
        self.get_args("0.0.0.0 8000")  # min значение
        self.assertEqual(get_client_param(), ("0.0.0.0", 8000))

        self.get_args("255.255.255.255 7890")  # мах значение
        self.assertEqual(get_client_param(), ("255.255.255.255", 7890))

        self.get_args("256.256.256.256")  # превышены значения в ip адресе
        with self.assertRaises(SystemExit) as cm:
            get_client_param()
        self.assertGreater(cm.exception.code, 0)

        self.get_args("")  # пропущены все параметры
        with self.assertRaises(SystemExit) as cm:
            get_client_param()
        self.assertGreater(cm.exception.code, 0)

        self.get_args("localhost zzz")  # port не число
        with self.assertRaises(SystemExit) as cm:
            get_client_param()
        self.assertGreater(cm.exception.code, 0)

        self.get_args("localhost")  # пропущен необязательный параметр (port, по умолчанию 7777)
        self.assertEqual(get_client_param(), ("localhost", 7777))


if __name__ == "__main__":
    unittest.main()
