import dis
from io import StringIO

from client import Client
from server import Server

""" 1.  Реализовать метакласс MetaVerifier, выполняющий базовую проверку класса "Client" и "Server"(для проверок уместно
        использовать модуль dis). Для клиента проверить:
            - отсутствие вызовов accept и listen для сокетов;   '(accept)': False, '(listen)': False
            - использование сокетов для работы по TCP;          '(SOCK_STREAM)': True
            - отсутствие создания сокетов на уровне классов.    '(socket)': True
    2.  Для сервера проверить:
            - отсутствие вызовов connect для сокетов;           '(connect)': False
            - использование сокетов для работы по TCP.          '(SOCK_STREAM)': True
"""


class MetaVerifier(type):
    """ Считываем в строку результат dis - дизассемблирования заданного объекта """
    @staticmethod
    def get_byte_code(obj: type) -> str:
        with StringIO() as out:
            dis.dis(obj, file=out)
            return out.getvalue()

    def __call__(cls, *args, **kwargs):
        """ Из последней колонки выбираем только значения, совпадающие с заданными для поиска.
            Записываем результат в атрибут 'search_result' создаваемого класса.  """
        keys = list(args[1].keys())
        li = [y for x in cls.get_byte_code(args[0]).split('\n') if x and (y := x.split()[-1]) in keys]
        setattr(cls, 'search_result', li)
        return super().__call__(*args, **kwargs)


class BasicDisCheck(metaclass=MetaVerifier):
    """ Класс, порожденный метаклассом MetaVerifier с атрибутами:
        obj - исследуемый объект
        items_search - словарь key(строка для поиска): val(Boolean); True - должна быть, False - отсутствовать """
    def __init__(self, obj: type, items_search: dict):
        self.obj = obj
        self.items_search = items_search

    def __call__(self):
        sr = set(getattr(self, "search_result"))
        for k, v in self.items_search.items():
            print(f"Value {k} was{'' if k in sr else ' not'} found: - {'FAILED' if v ^ (k in sr) else 'PASSED'}")


""" 3.  Реализовать дескриптор для класса серверного сокета, а в нем — проверку номера порта. Это должно быть целое 
        число (>=0). Значение порта по умолчанию равняется 7777. Дескриптор надо создать в отдельном классе. Его
        экземпляр добавить в пределах класса серверного сокета. Номер порта передается в экземпляр дескриптора при
        запуске сервера."""


class PortDescriptor:
    @classmethod
    def verify_port(cls, port):
        if type(port) != int:
            raise TypeError("Порт должен быть задан целым числом")
        if not 1024 <= port <= 49151:
            raise ValueError("Порт может быть задан в пользовательском диапазоне от 1024 до 49151]")

    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, instance, owner):
        print("__get__")
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        print("__set__")
        self.verify_port(value)
        setattr(instance, self.name, value)


class ServerDescriptor:
    port = PortDescriptor()

    def __init__(self, address, port=7777):
        self.port = port
        self.server = Server(port=self.port)


if __name__ == "__main__":
    print('\nЗадание 1.\nПроверка класса Client:')
    BasicDisCheck(Client, {'(accept)': False, '(listen)': False, '(socket)': True, '(SOCK_STREAM)': True})()
    print('\nЗадание 2.\nПроверка класса Server:')
    BasicDisCheck(Server, {'(connect)': False, '(SOCK_STREAM)': True})()
    print('\nЗадание 3.\nПроверка класса Server:')
    z = ServerDescriptor(49151)
    print(f'{z.port=}')
    z.server.run()
