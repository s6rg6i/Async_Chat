import time
from pydantic import BaseModel, ValidationError, Field, validator, root_validator


# JIM: Команды, которые можно реализовать
# Register
# Login
# GetList
# Handshake
# Message
# Feed
# StatusOnline
# HandshakeKey
# HandshakeNotice
# FileAdd
# StorageFile
# GetFile

# “action”: “authenticate” — авторизация на сервере;
# “action”: “presence” — присутствие. Сервисное сообщение для извещения сервера о присутствии клиента online;
# “action”: “prоbe” — проверка присутствия. Сервисное сообщение от сервера для проверки присутствии клиента online;
# “action”: “quit” — отключение от сервера;
# “action”: “msg” — простое сообщение пользователю или в чат;
# “action”: “join” — присоединиться к чату;
# “action”: “leave” — покинуть чат.


# АУТЕНТИФИКАЦИЯ
class User(BaseModel):
    account_name: str
    password: str


class Login(BaseModel):
    action: str  # 'action': 'auth'
    time: float  # time in seconds since the Epoch: time.time(): float; time.ctime(time.time()): str;
    user_login: User

    @validator('action')  # отдельное поле
    def valid_name(cls, v: str) -> str:
        if v != 'auth':
            raise ValueError("'action' must be 'auth'")
        return v


class LogOut(BaseModel):
    action: str  # 'action': 'quit'


class ServerResponse(BaseModel):
    response: int
    message: str


# В СЕТИ/ НЕ В СЕТИ
class UserPresence(BaseModel):
    account_name: str
    status: str  # 'status': 'User is online'


class Presence(BaseModel):
    action: str  # 'action': 'presence'
    time: float
    type: str  # 'type': 'status'
    user: UserPresence

    @validator('action')  # отдельное поле
    def valid_name(cls, v: str) -> str:
        if v != 'presence':
            raise ValueError("'action' must be 'presence'")
        return v


class ServerProbe(BaseModel):
    action: str  # 'action': 'probe'
    time: float


# ОБМЕН СООБЩЕНИЯМИ
class Join(BaseModel):
    action: str  # 'action': 'join'
    time: float
    room: str  # 'room': 'room_name'


class Leave(BaseModel):
    action: str  # 'action': 'leave'
    time: float
    room: str  # 'room': 'room_name'


class Message(BaseModel):
    action: str  # 'action': 'msg'
    time: float
    to: str  # 'str': 'room_name',
    author: str  # 'author': 'account_name'
    message: str


class Member:
    def __init__(self, user: str, psw='psw', room='Python console chat'):
        self.user = user
        self.psw = psw
        self.room = room

    def login(self) -> Login:
        return Login(action='auth', time=time.time(), user_login=User(account_name=self.user, password=self.psw))

    def join(self) -> Join:
        return Join(action='join', time=time.time(), room=self.room)

    def message(self, msg: str) -> Message:
        return Message(action='msg', time=time.time(), author=self.user, to=self.room, message=msg)

    def leave(self) -> Leave:
        return Leave(action='leave', time=time.time(), room=self.room)


def get_unix_time_str():
    t1 = time.time()
    print(type(t1))
    unix_time_str = time.ctime(t1) + '\n'
    return unix_time_str


if __name__ == "__main__":
    # print(get_unix_time_str())
    m = Member('user1', '1', 'my chat')
    print(m.login().json())
    print(m.join().json())
    msg0 = m.message('Привет!!!')
    print(b0 := msg0.json())
    print(m.leave().json())

    obj0 = Message.parse_raw(b0)  # byte -> <class '__main__.Message'>
    print(dict(obj0))
    print(type(obj0), obj0)

    s0 = '{"response": 200, "alert": "By!"}'
    s1 = {"action": "msg", "time": 1666019000.2856922, "to": "chat", "author": " srg", "message": "Hi admin"}
