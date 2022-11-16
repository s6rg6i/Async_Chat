## 10. Дескрипторы и метаклассы

### Практическое задание
 
---  

#### Продолжение работы с проектом «Мессенджер»:

1. Реализовать метакласс ClientVerifier, выполняющий базовую проверку класса «Клиент» (для некоторых проверок уместно использовать модуль dis):
    - отсутствие вызовов accept и listen для сокетов;
    - использование сокетов для работы по TCP;
    - отсутствие создания сокетов на уровне классов, то есть отсутствие конструкций такого вида:
    
```Python
class Client:
s = socket()
...
```

2. Реализовать метакласс ServerVerifier, выполняющий базовую проверку класса «Сервер»:
    - отсутствие вызовов connect для сокетов;

    - использование сокетов для работы по TCP.

3. Реализовать дескриптор для класса серверного сокета, а в нем — проверку номера порта. Это должно быть целое число (>=0). Значение порта по умолчанию равняется 7777. Дескриптор надо создать в отдельном классе. Его экземпляр добавить в пределах класса серверного сокета. Номер порта передается в экземпляр дескриптора при запуске сервера.

---