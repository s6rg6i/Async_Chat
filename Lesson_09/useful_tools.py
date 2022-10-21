import ipaddress
import socket
import subprocess
from collections import namedtuple
import chardet
import tabulate


def get_ip_address(host: str) -> str:
    try:
        return str(ipaddress.ip_address(host))  # по условию задачи: проверка корректности ip адреса
    except ValueError:
        try:  # Возможно задано доменное имя - получим ip адрес
            return socket.gethostbyname_ex(host)[2][0]  # ('google.com', [], ['172.217.16.14']) ([]: aliases)
        except socket.gaierror:  # не ip адрес и не доменное имя
            return ''


def host_ping(hosts: list):
    Result, results = namedtuple('Result', 'host ip is_access'), []
    for host in hosts:
        if ip := get_ip_address(host):
            res = subprocess.Popen(["ping", ip, "-n", "1", "-w", "100"], stdout=subprocess.PIPE).communicate()[0]
            enc = chardet.detect(res)["encoding"]
            res = res.decode(encoding=enc)
            # is_access = False if '100% потерь' in res else True
            is_access = not ('100% потерь' in res)
        else:
            ip, is_access = 'impossible', False
        results.append(Result(host, ip, is_access))
    return results


# В качестве итератора можно было использовать сеть с заданной маской подсети, нпр.
# [print(addr) for addr in ipaddress.ip_network('10.1.0.0/30')]
# но в этом случае диапазон, определенный маской, кратен 2**n, поэтому решил сделать перебор [start, end]
def host_range_ping(host: str, start=1, end=254):  # корректные адреса хостов (исключаем базовый и широковещательный)
    if not (0 < start < 255 or 0 < end < 255):
        print('Корректный диапазон адресов в пределах: [1:254] ')
    if not (ip := get_ip_address(host)):
        print('Некорректно задан хост')
    start = 1 if start < 1 else 254 if start > 254 else start
    end = 1 if end < 1 else 254 if end > 254 else end  # 'Корректируем диапазон адресов последнего октета: [1:254] '
    start, end = (start, end) if start < end else (end, start)
    base_ip = ip[:ip.rfind('.')]  # первые 3 октета ip адреса
    return host_ping([f'{base_ip}.{i}' for i in range(start, end + 1)])


def host_range_ping_tab(host: str, start=1, end=254):
    hosts = host_range_ping(host, start, end)
    result_dict = {'Узел доступен': [f'host:{h.host} ip:{h.ip}' for h in hosts if h.is_access],
                   'Узел недоступен': [f'host:{h.host} ip:{h.ip}' for h in hosts if not h.is_access]}
    print(tabulate.tabulate(result_dict, headers="keys"))


print('\n~~~~~~~~~~ Задание 1 ~~~~~~~~~~')
host_list = ['google.com', '10.0.0.255', 'localhost', 'gb.ru', '192.168.0.256', 'ru.ru', '']
pings = host_ping(host_list)
[print(f'host:{h.host:20} ip:{h.ip:15} => {"Узел доступен" if h.is_access else "Узел недоступен"}') for h in pings]

print('\n~~~~~~~~~~ Задание 2 ~~~~~~~~~~')
pings = host_range_ping(socket.gethostname(), start=1, end=5)
[print(f'ip:{h.ip:15} => {"Узел доступен" if h.is_access else "Узел недоступен"}') for h in pings]

print('\n~~~~~~~~~~ Задание 3 ~~~~~~~~~~')
host_range_ping_tab('192.168.100.1', start=1, end=5)
