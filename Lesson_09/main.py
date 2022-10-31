from pathlib import Path
from subprocess import Popen, CREATE_NEW_CONSOLE

try:
    num = int(input("Задайте количество запускаемых клиентских приложений(по умолчанию 2): "))
except ValueError:
    num = 0
num = num if 0 < num < 10 else 2

# полный путь к python.exe из venv, тк установлена внешняя библиотека pydantic
python_bin = Path(__file__).resolve().parent.parent / 'venv/Scripts/python.exe'

print('Запускаем сокет-сервер...')  # запускаем сервер отдельным процессом
p_list = [Popen('python server.py', creationflags=CREATE_NEW_CONSOLE)]

print(f'Запускаем {num} сокет-клиентов...')  # запускаем 2 клиента отдельными процессами
p_list = [*p_list, *[Popen([python_bin, 'client.py'], creationflags=CREATE_NEW_CONSOLE) for _ in range(num)]]

while input("Закрыть клиентов и выйти (q) ").lower() not in 'qQйЙ':  # Выход: <q><enter>
    ...
[p.kill() for p in p_list]  # удаляем запущенные процессы
