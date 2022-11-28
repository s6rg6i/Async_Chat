import time
from json import dumps
import rsa
from base64 import b64encode, b64decode

from constants import Permission, ACT_MSG

"""  Задание 1, 2.
1. Реализовать аутентификацию пользователей на сервере.
2. Реализовать хранение паролей в БД сервера (пароли не хранятся в открытом виде — хранится хэш-образ от пароля
   с добавлением криптографической соли)."""

# Аутентификация на сервере реализована в классе MessageParser метод login(), файл server.py. В нем же и регистрация
# нового пользователя. Хранение паролей и соли - в таблице 'users', поля password и salt. Динамическая соль и
# hash пароля формируются в методе hash_password(), класс ChatDb, файл storage.py.

""" Задание 3.
3. Реализовать декоратор @login_required, проверяющий авторизацию пользователя для выполнения той или иной функции."""


# Т.к. программа 'чат' уже предполагает необходимость авторизации для работы, заменил декоратор @login_required на
# @permissions_checking с параметрами доступа. Декоратор добавляет jim-сообщению ключ 'access' с необходимыми
# разрешениями для проверки сервером права доступа

def permissions_checking(access: int):
    def decorator(function):
        def wrapper(*args, **kwargs):
            result = function(*args, **kwargs)
            return f'{result[:-1]}, "access": {access}}}'

        return wrapper

    return decorator


# 4. * Реализовать возможность сквозного шифрования сообщений (использовать асимметричный
#    шифр, ключи которого хранятся только у клиентов).

# В моей реализации чата предполагалось, что создается приватная комната. И сервер у каждого присоединившегося
# запрашивает публичный ключ (клиент формирует или отправляет готовый) и отдает всем участникам комнаты. Клиент
# формирует отдельное сообщение, зашифрованное соответствующим открытым ключом, для каждого участника комнаты.
# Примерная реализация ниже.

class RSAEncryption:
    def __init__(self):
        self.pub, self.private = rsa.newkeys(2048)

    @staticmethod
    def encrypt(msg: str, pub_user: rsa.PublicKey) -> str:
        text = b64encode(msg.encode())
        print(len(text))
        try:
            b64_msg = rsa.encrypt(text, pub_user)  # шифруем сообщение публичным ключом получателя
            return b64encode(b64_msg).decode()
        except OverflowError as e:   # превышена максимальная длина сообщения для ключа
            print(e)
            return ''

    def decrypt(self, msg):
        cipher = b64decode(msg.encode())
        b64_msg = rsa.decrypt(cipher, self.private)
        return b64decode(b64_msg).decode()


if __name__ == '__main__':
    print('Работа декоратора')

    @permissions_checking(Permission.WRITE | Permission.READ)
    def message0(msg: str) -> str:  # "action": "msg" — простое сообщение пользователю или в чат;
        return dumps(dict(action=ACT_MSG, time=time.time(), author="user", to="room", message=msg))


    def message1(msg: str) -> str:  # "action": "msg" — простое сообщение пользователю или в чат;
        return dumps(dict(action=ACT_MSG, time=time.time(), author="user", to="room", message=msg))

    print(message0('Hi there'))  # с декоратором
    # {"action": "msg", "time": 1669623736.4304502, "author": "user", "to": "room", "message": "Hi there", "access": 3}
    print(message1('Hi there'))  # без декоратора
    # {"action": "msg", "time": 1669623736.4304502, "author": "user", "to": "room", "message": "Hi there"}

    print('Работа RSA шифрования')
    print('Получаем открытый и закрытый ключ пользователя')
    user_rsa = RSAEncryption()
    public_user = user_rsa.pub
    print('Получаем открытый и закрытый ключ отправителя')
    my_rsa = RSAEncryption()

    # для ключа длиной 2048 длину сообщения придется ограничить 120 символами
    message = 'Сообщение, переданное user, зашифрованное публичным ключом user'
    print(f'{len(message)=}')

    enc_message = my_rsa.encrypt(message, public_user)  # посылаем сообщение to user
    print(f'{enc_message=}')
    dec_message = user_rsa.decrypt(enc_message)  # user расшифровывает своим приватным ключом
    print(f'{dec_message=}')
