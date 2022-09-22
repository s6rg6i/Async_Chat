import subprocess
import sys

import chardet

# 01.1. Каждое из слов «разработка», «сокет», «декоратор» представить в строковом формате и проверить тип и
#       содержание соответствующих переменных. Затем с помощью онлайн-конвертера преобразовать строковые представление
#       в формат Unicode и также проверить тип и содержимое переменных.

print("\n~~~ task 1 ~~~")
[print(f"{x:12}: type {type(x)}") for x in ("разработка", "сокет", "декоратор")]
[
    print(f"{u}: type {type(x)}")
    for x, u in zip(
        (
            "\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",  # 'разработка' в формате Unicode
            "\u0441\u043e\u043a\u0435\u0442",  # сокет
            "\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440",  # декоратор
        ),
        (
            r"\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430",  # Строковое представление для вывода
            r"\u0441\u043e\u043a\u0435\u0442",
            r"\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440",
        ),
    )
]

# 01.2. Каждое из слов «class», «function», «method» записать в байтовом типе без преобразования в последовательность
#       кодов (не используя методы encode и decode) и определить тип, содержимое и длину соответствующих переменных.

print("\n~~~ task 2 ~~~")
[print(f"{x}: type {type(x)} len {len(x)}") for x in (b"class", b"function", b"method")]

# 01.3. Определить, какие из слов «attribute», «класс», «функция», «type» невозможно записать в байтовом типе.

print("\n~~~ task 3 ~~~")
for enc in ("utf-8", "ascii"):
    print(f"---- encoding={enc}:")
    for val in ("attribute", "класс", "функция", "type"):
        try:
            print(f"str '{val}': {bytearray(val, encoding=enc)}")
        except UnicodeError:
            print(f'str "{val}" cannot be presented as a bytes type with encoding="{enc}"')

# 01.4. Преобразовать слова «разработка», «администрирование», «protocol», «standard» из строкового представления
#       в байтовое и выполнить обратное преобразование (используя методы encode и decode)

print("\n~~~ task 4 ~~~")
for val in ("разработка", "администрирование", "protocol", "standard"):
    val_encoded = val.encode("utf-8")
    val_decoded = val_encoded.decode("utf-8")
    print(val_encoded, type(val_encoded))
    print(f'"{val_decoded}" {type(val_decoded)}')

# 01.5. Выполнить пинг веб-ресурсов yandex.ru, youtube.com и преобразовать результаты из байтовового в строковый тип
#       на кириллице.

print("\n~~~ task 5 ~~~")
for url in ("yandex.ru", "youtube.com"):
    lst = [line for line in subprocess.Popen(("ping", url, "-n", "1"), stdout=subprocess.PIPE).communicate()]
    encoding = chardet.detect(lst[0])["encoding"]
    print(f"Кодировка: {encoding}\n{lst[0].decode(encoding=encoding)}")

# 01.6. Создать текстовый файл test_file.txt, заполнить его тремя строками: «сетевое программирование», «сокет»,
#       «декоратор». Проверить кодировку файла по умолчанию. Принудительно открыть файл в формате Unicode и вывести
#       его содержимое.

print("\n~~~ task 6 ~~~")
with open("test_file.txt", "rb") as file:
    txt_bytes = file.read()
encoding = chardet.detect(txt_bytes)["encoding"]
print(f"Кодировка: {encoding}\nDecoded file 'test_file.txt':\n{txt_bytes.decode(encoding=encoding)}")
