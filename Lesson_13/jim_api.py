import time
from json import dumps


class Jim:
    def __init__(self, user: str, psw='psw', room='My chat'):
        self.user = user
        self.psw = psw
        self.room = room

    def login(self) -> str:  # "action": "auth" — авторизация на сервере
        return dumps(dict(action='auth', time=time.time(), user_login=dict(account_name=self.user, password=self.psw)))

    def join(self) -> str:  # "action": "join" — присоединиться к чату
        return dumps(dict(action='join', time=time.time(), room=self.room))

    def message(self, msg: str) -> str:  # "action": "msg" — простое сообщение пользователю или в чат;
        return dumps(dict(action='msg', time=time.time(), author=self.user, to=self.room, message=msg))

    def presence(self) -> str:  # — присутствие. Сообщение для сервера о присутствии клиента online;
        return dumps(dict(
            action='presence', time=time.time(), type='status', user=dict(account_name=self.user, status="I'm here")))

    def leave(self) -> str:  # "action": "leave" — покинуть чат. (@@leave)
        return dumps(dict(action='leave', time=time.time(), room=self.room))

    def del_contact(self, user_id: str) -> str:  # "action": "del_contact" -контакт в список контактов (@@del_contact)
        return dumps(dict(action='del_contact', user_id=user_id, time=time.time(), user_login=self.user))

    def add_contact(self, user_id: str) -> str:  # "action": "add_contact" +контакт в список контактов (@@add_contact)
        return dumps(dict(action='add_contact', user_id=user_id, time=time.time(), user_login=self.user))

    def get_contacts(self) -> str:  # "action": "get_contacts" — получить список пользователей чата (@@get_list)
        return dumps(dict(action='get_contacts', time=time.time(), user_login=self.user))

    def get_messages(self) -> str:  # "action": "get_messages" — получить n последних сообщений чата (@@get_messages)
        return dumps(dict(action='get_messages', time=time.time(), room=self.room))

    @staticmethod
    def quit() -> str:  # "action": "quit" — отключение от сервера (@@quit)
        return dumps(dict(action='quit'))

    @staticmethod
    def probe() -> str:  # "action": "probe" - запрос отправляет сервер, клиент отвечает "presence"
        return dumps(dict(action='probe', time=time.time()))

    @staticmethod
    def response_ok(msg: str) -> str:  # Сообщение-ответ сервера: успешное завершение
        return dumps(dict(response=200, time=time.time(), alert=msg))

    @staticmethod
    def response_err(code: int, msg: str):  # Сообщение-ответ сервера: ошибка
        return dumps(dict(response=code, time=time.time(), error=msg))

    @staticmethod
    def user_list(lst: list):  # Сообщение-ответ сервера: список пользователей
        return dumps(dict(response=298, time=time.time(), user_list=lst))
