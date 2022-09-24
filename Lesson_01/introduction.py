# Освежите в памяти работу с генераторами и итераторами: как работают, как их использовать, как написать свой.
# https://docs.python.org/3.8/library/stdtypes.html#iterator-types
# https://docs.python.org/3.8/library/stdtypes.html#generator-types
# https://docs.python.org/3.8/reference/expressions.html#yieldexpr
# Каждый из вариантов реализуйте в виде класса и в виде функций с использованием оператора yield.
# Попробуйте реализовать FizzBuzz в виде генератора. Делители передавать в качестве параметров.
# Использование такого генератора будет выглядеть примерно так:
# for i in fizzbuzz(fizz=3, buzz=5):
#     print(i)

# Генератор FizzBuzz в виде класса
class FizzBuzz:
    def __init__(self, fizz=3, buzz=5, quantity=16):
        self.quantity = quantity
        self.fizz = fizz
        self.buzz = buzz

    def __iter__(self):
        num = 0
        while num < self.quantity:
            yield "Fizz" * (num % self.fizz == 0) + "Buzz" * (num % self.buzz == 0) or num
            num += 1


# Генератор fizz_buzz в виде функции
def fizz_buzz(fizz=3, buzz=5, quantity=16):
    num = 0
    while num < quantity:
        yield "Fizz" * (num % fizz == 0) + "Buzz" * (num % buzz == 0) or num
        num += 1


# Генератор gen в виде generator expression
gen = ("Fizz" * (num % 3 == 0) + "Buzz" * (num % 5 == 0) or num for num in range(16))


# Coroutine
def fizzbuzz_cor():
    while True:
        num = yield
        print("Fizz" * (num % 3 == 0) + "Buzz" * (num % 5 == 0) or num, end=" ")


print("\nГенератор в виде класса")
for x in FizzBuzz():
    print(x, end=" ")

print("\nГенератор в виде функции")
for x in fizz_buzz():
    print(x, end=" ")

print("\nГенератор в виде выражения-генератора")
for x in gen:
    print(x, end=" ")

print("\nКорутин")
f = fizzbuzz_cor()
f.send(None)
for i in range(16):
    f.send(i)
