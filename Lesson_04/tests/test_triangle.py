import unittest
from Lesson_04.triangle import Triangle


class TriangleTest(unittest.TestCase):
    def setUp(self) -> None:
        self.tr0 = Triangle(3, 4, 5)  # OK
        self.tr1 = Triangle("3", "4", "5")  # OK
        self.tr2 = Triangle(666777888.9, 999888777, 444555999.888)  # OK
        self.tr3 = Triangle(3, "5.ooo4", 5)  # "5.ooo4" нельзя преобразовать в число
        self.tr4 = Triangle(1, 2, 3)  # 3 = 1 + 2
        self.tr5 = Triangle(1, -2, 3)  # отрицательное
        self.tr6 = Triangle(2, 2, 2, 3)  # больше 3 сторон
        self.tr7 = Triangle(2, 2)  # меньше 2 сторон
        self.tr8 = Triangle()  # нет сторон

    def test_0(self):
        self.assertEqual(self.tr0.sides, [3.0, 4.0, 5.0])

    def test_1(self):
        self.assertEqual(self.tr1.sides, [3.0, 4.0, 5.0])

    def test_2(self):
        self.assertEqual(self.tr2.sides, [444555999.888, 666777888.9, 999888777.0])

    def test_3(self):
        self.assertEqual(self.tr3, None)

    def test_4(self):
        self.assertEqual(self.tr4, None)

    def test_5(self):
        self.assertEqual(self.tr5, None)

    def test_6(self):
        self.assertEqual(self.tr6, None)

    def test_7(self):
        self.assertEqual(self.tr7, None)

    def test_8(self):
        self.assertEqual(self.tr8, None)


if __name__ == "__main__":
    unittest.main()
