"""
Тестирование сортировок.
"""

import random
import unittest
from abc import ABC

from sorts.introsort import optimized_introsort, _median_sep_index, introsort
from sorts.quicksort import _partition, _3_way_partition, quick_sort_random, \
    quick_sort_no_tail_recursion, quick_sort_3_way_partition, \
    quick_sort_no_recursion


class PartitionTests(unittest.TestCase):

    def verify_list(self, lst, pos):
        for i in range(len(lst)):
            if i <= pos:
                self.assertLessEqual(lst[i], lst[pos])
            else:
                self.assertGreater(lst[i], lst[pos])

    def test_partition(self):
        for _ in range(100):
            lst = [random.randint(0, 40) for _ in range(100)]
            pos = _partition(lst, 0, len(lst) - 1)
            self.verify_list(lst, pos)


class Partition3WaysTests(unittest.TestCase):

    def verify_list(self, lst, k1, k2):
        for i in range(len(lst)):
            if i < k1:
                self.assertLessEqual(lst[i], lst[k1])
            elif k1 <= i < k2:
                self.assertEqual(lst[i], lst[k1])
            else:
                self.assertGreater(lst[i], lst[k1])

    def test_partition(self):
        for _ in range(100):
            lst = [random.randint(0, 40) for _ in range(100)]
            k1, k2 = _3_way_partition(lst, 0, len(lst) - 1)
            self.verify_list(lst, k1, k2)


class MedianSepIndexTests(unittest.TestCase):

    def test_all(self):
        self.assertEqual(_median_sep_index([1, 2, 3], 0, 2), 1)
        self.assertEqual(_median_sep_index([3, 2, 1], 0, 2), 1)
        self.assertEqual(_median_sep_index([2, 3, 1], 0, 2), 0)
        self.assertEqual(_median_sep_index([2, 2, 1], 0, 2), 0)
        self.assertEqual(_median_sep_index([1, 2, 2], 0, 2), 1)


class SortTests(ABC):

    def verify(self, lst):
        self.func(lst)
        self.assertEqual(lst, sorted(lst))

    def test_static_combinations(self):
        self.verify([])
        self.verify([1])
        self.verify([1, 2])
        self.verify([2, 1])
        self.verify([1, 1, 2])
        self.verify([1, 2, 1])
        self.verify([2, 1, 1])
        self.verify([2, 1, 4, 3, 3, 5])
        self.verify([5, 3, 2, 3, 1, 4])
        self.verify([3, 3, 2, 1, 4, 5])
        self.verify([3, 3, 2, 1, 6, 4, 5])
        self.verify([3, 3, 2, 1, 2, 2, 5, 6, 4, 5])

    def test_on_random_lists(self):
        for _ in range(100):
            lst = [random.randint(0, 25) for _ in range(100)]
            self.verify(lst)


class RandomQuickSortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = quick_sort_random


class NoTailQuickSortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = quick_sort_no_tail_recursion


class ThreeWayPartitionQuickSortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = quick_sort_3_way_partition


class NoRecursionQuickSortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = quick_sort_no_recursion


class IntrosortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = introsort


class OptimizedIntrosortTests(SortTests, unittest.TestCase):
    def setUp(self):
        self.func = optimized_introsort


if __name__ == '__main__':
    unittest.main()
