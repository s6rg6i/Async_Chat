Модуль server_db.py documentation
=================================

Модуль Создает БД со следующими таблицами:
__________________________________________

- Пользователи: users(id, login, password, salt, public_key
- Комнаты: Room(id, name)
- История подключений: History(id, time, ip, user_id)
- Список комнат и пользователей: RoomUser(room_id, user_id, permission)
- Сообщения чата: Message(id, room_id, user_id, msg, time)




class ChatDb
~~~~~~~~~~~~
.. autoclass:: server_db.ChatDb
    :members:

