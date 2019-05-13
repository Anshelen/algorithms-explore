"""
Порядковые статистики. Надо найти элемент, который равен k-ому в отсортированном
массиве. Время поиска в среднем линейное.
"""

import unittest

from sorts.partitions import three_way_partition


def find(lst, k):
    if not lst or k < 1 or k > len(lst):
        raise IndexError

    def _find(lst, l, r, k):
        if l >= r:
            return lst[l]
        k1, k2 = three_way_partition(lst, l, r)
        if l <= k < k1:
            return _find(lst, l, k1, k)
        elif k1 <= k < k2:
            return lst[k1]
        else:
            return _find(lst, k2, r, k)

    return _find(lst, 0, len(lst) - 1, k - 1)


class Tests(unittest.TestCase):

    def test_empty_list(self):
        with self.assertRaises(IndexError):
            find([], 1)

    def test_big_index(self):
        with self.assertRaises(IndexError):
            find([1], 2)

    def test_zero_index(self):
        with self.assertRaises(IndexError):
            find([1], 0)

    def test_negative_index(self):
        with self.assertRaises(IndexError):
            find([1], -1)

    def test_common(self):
        self.assertEqual(find([1, 1], 1), 1)
        self.assertEqual(find([1, 2], 1), 1)
        self.assertEqual(find([2, 1], 1), 1)
        self.assertEqual(find([2, 1], 2), 2)
        self.assertEqual(find([1, 2, 3], 1), 1)
        self.assertEqual(find([3, 2, 1], 1), 1)
        self.assertEqual(find([3, 2, 1], 2), 2)
        self.assertEqual(find([3, 2, 1], 3), 3)
        self.assertEqual(find([2, 2, 1], 3), 2)
        self.assertEqual(find([2, 2, 1], 2), 2)
        self.assertEqual(find([2, 2, 1], 1), 1)
        self.assertEqual(find([0, 1, 4, 3, 2], 1), 0)

    def test_dynamic(self):
        import random
        for _ in range(50):
            lst = [random.randrange(35) for _ in range(random.randrange(50))]
            s_lst = sorted(lst)
            for i in range(1, len(lst)):
                self.assertEqual(find(lst[:], i), s_lst[i - 1])


if __name__ == '__main__':
    unittest.main()
