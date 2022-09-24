"""
2.  Есть файл orders в формате JSON с информацией о заказах. Написать скрипт, автоматизирующий его заполнение данными.
a.  Создать функцию write_order_to_json(), в которую передается 5 параметров — товар (item), количество (quantity),
    цена (price), покупатель (buyer), дата (date). Функция должна предусматривать запись данных в виде словаря в файл
    orders.json. При записи данных указать величину отступа в 4 пробельных символа;
b.  Проверить работу программы через вызов функции write_order_to_json() с передачей в нее значений каждого параметра.
"""

import json
import os


def write_order_to_json(keys, vals, f_name="orders.json"):
    orders = {}
    if os.path.exists(f_name):  # если файл не существует, создадим его ниже, open(f_name, 'w')
        with open(f_name, "r", encoding="utf-8") as file:
            orders = json.load(file)
    with open(
        f_name,
        "w",
        encoding="utf-8",
    ) as file:
        orders.setdefault("orders", []).append({key: val for key, val in zip(keys, vals)})
        json.dump(orders, file, indent=4, ensure_ascii=False)


order_keys = ("item", "quantity", "price", "buyer", "date")

for data in (
    ("Планшет", "20", "15000", "Иванов", "20.09.2022"),
    ("МФУ", "2", "25000", "Петров", "20.09.2022"),
    ("Сканер", "3", "20000", "Сидоров", "20.09.2022"),
):
    write_order_to_json(order_keys, data)
