from pathlib import Path
from subprocess import Popen, CREATE_NEW_CONSOLE

# полный путь к python.exe из venv, тк установлена внешняя библиотека pydantic
python_bin = Path(__file__).resolve().parent.parent / 'venv/Scripts/python.exe'

print('Сокет-сервер запущен!')  # запускаем сервер отдельным процессом
p_list = [Popen('python server.py', creationflags=CREATE_NEW_CONSOLE)]

print('2 Сокет-клиента запущены!')  # запускаем 2 клиента отдельными процессами
p_list = [*p_list, *[Popen([python_bin, 'client.py'], creationflags=CREATE_NEW_CONSOLE) for _ in range(2)]]

while input("Закрыть клиентов и выйти (q) ").lower() != 'q':  # Выход: <q><enter>
    ...
[p.kill() for p in p_list]  # удаляем запущенные процессы
