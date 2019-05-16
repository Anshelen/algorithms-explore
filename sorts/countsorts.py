"""
Сортировки, основанные на подсчете. Имеют сложность O(n).
"""

import random
import unittest
from typing import List


def countsort(lst: List, m: int, func=lambda x: x):
    """
    Стабильная сортировка подсчетом не на месте. Сортирует массив, состоящий
    из чисел в диапазоне [0, m). Принимает функцию, которая позволяет определить
    ключ элемента.
    """
    c = [0 for _ in range(m)]
    for el in lst:
        c[func(el)] += 1
    for i in range(1, len(c)):
        c[i] += c[i - 1]
    res = [None for _ in range(len(lst))]
    for i in range(len(lst) - 1, -1, -1):
        el = lst[i]
        res[c[func(el)] - 1] = el
        c[func(el)] -= 1
    return res


def digitsort(lst: List, d: int):
    """
    Сортирует подсчетом целые десятичные числа. Сложность О(d*n). Сортировка
    стабильная, не на месте.

    :param lst: список десятичных чисел
    :param d: максимальное количество разрядов в числах
    :return: отсортированный массив
    """

    def get_digit(x, n):
        """ Возвращает n-ную цифру в числе x. """
        return (x % (10 ** n)) // (10 ** (n - 1))

    for i in range(d):
        lst = countsort(lst, 10, func=lambda x: get_digit(x, i + 1))
    return lst


class CountSortTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(countsort([], 1), [])

    def test_stability(self):
        lst = [(1, 3), (1, 2), (1, 4), (0, 2), (2, 3)]
        expected = [(0, 2), (1, 3), (1, 2), (1, 4), (2, 3)]
        self.assertEqual(countsort(lst, 3, func=lambda x: x[0]), expected)

    def test_dynamic(self):
        for _ in range(100):
            m = 30
            lst = [random.randint(0, m - 1) for _ in
                   range(random.randint(0, 50))]
            self.assertEqual(countsort(lst, m), sorted(lst))


class DigitSortTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(digitsort([], 1), [])

    def test_common(self):
        lst = [267, 507, 912, 215, 109, 213, 199, 216, 257]
        self.assertEqual(digitsort(lst, 3), sorted(lst))

    def test_different_digit_amount(self):
        lst = [1777, 111, 94, 37, 111, 111, 15, 2, 0]
        self.assertEqual(digitsort(lst, 4), sorted(lst))

    def test_dynamic(self):
        for _ in range(100):
            m = 4
            lst = [random.randint(0, 10 ** m - 1) for _ in
                   range(random.randint(0, 50))]
            self.assertEqual(digitsort(lst, m), sorted(lst))


if __name__ == '__main__':
    unittest.main()
