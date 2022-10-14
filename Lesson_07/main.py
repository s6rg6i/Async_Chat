from subprocess import Popen, CREATE_NEW_CONSOLE


print('Сокет-сервер запущен!')  # запускаем сервер отдельным процессом
p_list = [Popen('python server.py', creationflags=CREATE_NEW_CONSOLE)]

print('3 Сокет-клиента запущены!')  # запускаем 3 клиента отдельными процессами
p_list = [*p_list, *[Popen('python client.py', creationflags=CREATE_NEW_CONSOLE) for _ in range(3)]]

while input("Закрыть клиентов и выйти (q) ").lower() != 'q':  # Выход: <q><enter>
    ...
[p.kill() for p in p_list]  # удаляем запущенные процессы
