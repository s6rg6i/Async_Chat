"""
3.  Написать скрипт, автоматизирующий сохранение данных в файле YAML-формата. Для этого:
a.  Подготовить данные для записи в виде словаря, в котором первому ключу соответствует список, второму — целое число,
    третьему — вложенный словарь, где значение каждого ключа — это целое число с юникод-символом, отсутствующим в
    кодировке ASCII (например, €);
b. Реализовать сохранение данных в файл формата YAML — например, в файл file.yaml. При этом обеспечить стилизацию файла
    с помощью параметра default_flow_style, а также установить возможность работы с юникодом: allow_unicode = True;
c.  Реализовать считывание данных из созданного файла и проверить, совпадают ли они с исходными.
"""

import yaml


# для решения проблемы: "родитель и его элементы списка находятся на одном уровне" воспользовался
# https://habr.com/ru/post/669684/?ysclid=l8ex9qb8z6262853544
class IndentDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(IndentDumper, self).increase_indent(flow, False)


am_money = {
    "banknotes": {"USA": ["1", "2", "5", "10", "20", "50", "100"]},
    "coins": {
        "1¢": "penny",
        "5¢": "nickel",
        "10¢": "dime",
        "¼$": "quarter",
        "½$": "half",
    },
    "implemented": 1792,
}

with open("file.yaml", "w", encoding="utf-8") as file:
    yaml.dump(am_money, file, Dumper=IndentDumper, default_flow_style=False, allow_unicode=True, sort_keys=False)

# при использовании BaseLoader, <'implemented': 1792> считывался как <'implemented': '1792'> и assert выдавал ошибку
with open("file.yaml", "r", encoding="utf-8") as file:
    ret_am_money = yaml.load(file, Loader=yaml.SafeLoader)

assert am_money == ret_am_money
