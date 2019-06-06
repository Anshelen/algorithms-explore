import unittest
from abc import ABC

from structures.disjoint_sets import SumDisjointSets, CollectDisjointSets, \
    MathDisjointSets


class DisjointSetsTests(ABC):

    def test_make_set(self):
        self.sets.make_set(1)
        self.assertEqual(len(self.sets), 1)

    def test_make_set_unique(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set(3)
        self.assertNotEqual(id1, id2)

    def test_find_value_empty(self):
        with self.assertRaises(RuntimeError):
            self.sets.find_value(1)

    def test_find_root_id_different(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set(3)
        self.assertNotEqual(self.sets.find_root_id(id1),
                            self.sets.find_root_id(id2))

    def test_find_root_id_same(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set(3)
        self.sets.union(id1, id2)
        self.assertEqual(self.sets.find_root_id(id1),
                         self.sets.find_root_id(id2))

    def test_len_on_empty_sets(self):
        self.assertEqual(len(self.sets), 0)


class MathDisjointSetsTests(DisjointSetsTests, unittest.TestCase):

    def setUp(self):
        self.sets = MathDisjointSets()

    def test_find_value(self):
        with self.assertRaises(NotImplementedError):
            self.sets.find_value(1)

    def test_union(self):
        id1 = self.sets.make_set()
        id2 = self.sets.make_set()
        id3 = self.sets.make_set()
        self.sets.union(id1, id2)
        self.assertEqual(self.sets.find_root_id(id1),
                         self.sets.find_root_id(id2))
        self.assertNotEqual(self.sets.find_root_id(id1),
                            self.sets.find_root_id(id3))


class SumDisjointSetsTests(DisjointSetsTests, unittest.TestCase):

    def setUp(self):
        self.sets = SumDisjointSets()

    def test_find_value(self):
        _id = self.sets.make_set(1)
        self.assertEqual(self.sets.find_value(_id), 1)

    def test_union(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set(2)
        id3 = self.sets.make_set(3)
        self.sets.union(id1, id2)
        self.assertEqual(self.sets.find_value(id1), self.sets.find_value(id2))
        self.assertEqual(self.sets.find_value(id1), 3)
        self.assertEqual(self.sets.find_value(id3), 3)


class CollectDisjointSetsTests(DisjointSetsTests, unittest.TestCase):

    def setUp(self):
        self.sets = CollectDisjointSets()

    def test_make_set_list(self):
        _id = self.sets.make_set([1, 2])
        self.assertEqual(self.sets.find_value(_id), [1, 2])

    def test_make_set_tuple(self):
        _id = self.sets.make_set((1, 2))
        self.assertEqual(self.sets.find_value(_id), [1, 2])

    def test_make_empty_set(self):
        _id = self.sets.make_set()
        self.assertEqual(self.sets.find_value(_id), [])

    def test_make_set_simple_type(self):
        _id = self.sets.make_set(1)
        self.assertEqual(self.sets.find_value(_id), [1])

    def test_find_value(self):
        _id = self.sets.make_set(1)
        self.assertEqual(self.sets.find_value(_id), [1])

    def test_union(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set(2)
        id3 = self.sets.make_set(3)
        self.sets.union(id1, id2)
        self.assertEqual(self.sets.find_value(id1), self.sets.find_value(id2))
        self.assertEqual(self.sets.find_value(id1), [1, 2])
        self.assertEqual(self.sets.find_value(id3), [3])

    def test_union_empty_set(self):
        id1 = self.sets.make_set(1)
        id2 = self.sets.make_set()
        self.sets.union(id1, id2)
        self.assertEqual(self.sets.find_value(id1), self.sets.find_value(id2))
        self.assertEqual(self.sets.find_value(id1), [1])


if __name__ == '__main__':
    unittest.main()
