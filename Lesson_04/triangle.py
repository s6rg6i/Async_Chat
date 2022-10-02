class Triangle:
    def __init__(self, *sides):
        self.sides = [x for x in map(float, sorted(list(sides)))]

    @classmethod
    def _validate(cls, *sides):
        try:
            assert sides
            st = [x for x in map(float, sorted(list(sides)))]  # если не числа - TypeError
            assert len(st) == 3  # три стороны
            assert st[0] > 0  # стороны не отрицательные и не нулевые
            assert st[2] < st[0] + st[1]  # большая сторона меньше суммы оставшихся
        except (AssertionError, TypeError):
            return False
        return True

    def __new__(cls, *sides):
        if cls._validate(*sides):
            return super().__new__(cls)

    def __str__(self):
        return " ".join([str(x) for x in self.sides])


if __name__ == "__main__":
    print(Triangle("3", "4", "5"))
    print(Triangle(3, 4, 5))
    print(Triangle(1, 2, 3))
