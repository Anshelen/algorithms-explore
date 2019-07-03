import random
import unittest

from structures.sum_tree_set import SumTreeSet


class SumTreeSetTests(unittest.TestCase):

    def setUp(self):
        self.set = SumTreeSet()

    def fill(self, arr):
        for x in arr:
            self.set.put(x)

    def assertContains(self, arr):
        s_arr = sorted(arr)
        self.assertEqual(len(self.set), len(arr))
        for i in range(len(arr)):
            self.assertEqual(self.set.get(i), s_arr[i])

    def test_sum_subset_empty(self):
        self.fill([])
        self.assertEqual(self.set.subset_sum(2, 5), 0)
        self.assertContains([])

    def test_sum_subset_invalid_indexes(self):
        self.fill([1, 2, 5, 6, 7])
        with self.assertRaises(IndexError):
            self.set.subset_sum(5, 4)

    def test_sum_subset_one_key_contain(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(5, 5), 5)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_one_key_not_contain(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(4, 4), 0)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_middle(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(2, 6), 13)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_all_keys(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(1, 7), 21)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_no_keys(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(3, 4), 0)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_more_then_max(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(6, 10), 13)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_less_then_min(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(-2, 2), 3)
        self.assertContains([1, 2, 5, 6, 7])

    def test_sum_subset_less_then_min_and_more_then_max(self):
        self.fill([1, 2, 5, 6, 7])
        self.assertEqual(self.set.subset_sum(-2, 10), 21)
        self.assertContains([1, 2, 5, 6, 7])

    def test_dynamic(self):
        def count_real(k1, k2):
            s = 0
            for i in range(k1, k2 + 1):
                if 0 <= i <= 50:
                    s += i
            return s

        arr = [i for i in range(51)]
        self.fill(arr)
        for _ in range(150):
            k1 = random.randint(-10, 60)
            k2 = random.randint(k1, 60)
            self.assertEqual(self.set.subset_sum(k1, k2), count_real(k1, k2))
            self.assertContains(arr)


if __name__ == '__main__':
    unittest.main()
