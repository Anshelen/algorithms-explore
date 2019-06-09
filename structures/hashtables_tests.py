import random
import unittest

from structures.hashtables import ChainHashtable, OpenAddressingHashtable


class HashtablesTests:

    def test_get_empty(self):
        with self.assertRaises(KeyError):
            self.table[1]

    def test_get_with_collision(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        self.assertEqual(self.table[0], 0)
        self.assertEqual(self.table[1], 1)
        self.assertEqual(self.table[16], 16)

    def test_put_and_get(self):
        self.table[1] = 2
        self.assertEqual(self.table[1], 2)
        self.assertEqual(len(self.table), 1)

    def test_put_same_key(self):
        self.table[1] = 2
        self.table[1] = 3
        self.assertEqual(self.table[1], 3)
        self.assertEqual(len(self.table), 1)

    def test_remove_empty(self):
        with self.assertRaises(KeyError):
            del self.table[1]

    def test_remove(self):
        self.table[1] = 2
        del self.table[1]
        self.assertEqual(len(self.table), 0)

    def test_remove_with_collision_first(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        del self.table[0]
        self.assertEqual(self.table[1], 1)
        self.assertEqual(self.table[16], 16)

    def test_remove_with_collision_second(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        del self.table[1]
        self.assertEqual(self.table[0], 0)
        self.assertEqual(self.table[16], 16)

    def test_remove_with_collision_third(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        del self.table[16]
        self.assertEqual(self.table[0], 0)
        self.assertEqual(self.table[1], 1)

    def test_len(self):
        self.table[1] = 2
        self.table[2] = 3
        self.table[4] = 3
        self.assertEqual(len(self.table), 3)

    def test_len_with_collision(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        self.assertEqual(len(self.table), 3)

    def test_len_with_collision_after_delete(self):
        self.table[0] = 0
        self.table[1] = 1
        self.table[16] = 16
        del self.table[1]
        self.assertEqual(len(self.table), 2)

    def test_contains(self):
        self.table[1] = 2
        self.assertTrue(1 in self.table)
        self.assertFalse(2 in self.table)

    def test_dynamic(self):
        for _ in range(100):
            self.setUp()
            d = {}
            keys = set()
            for _ in range(50):
                k, v = random.randint(1, 100), random.randint(1, 100)
                self.table[k] = v
                d[k] = v
                keys.add(k)
            self.assertEqual(len(d), len(self.table))
            for key in keys:
                self.assertEqual(d[key], self.table[key])
            for key in keys:
                del self.table[key]
            self.assertEqual(len(self.table), 0)


class ChainHashTableTests(HashtablesTests, unittest.TestCase):

    def setUp(self):
        self.table = ChainHashtable()


class OpenAddressingHashTableTests(HashtablesTests, unittest.TestCase):

    def setUp(self):
        self.table = OpenAddressingHashtable()

    def test_overflow(self):
        for i in range(50):
            self.table[0] = i
            del self.table[0]


if __name__ == '__main__':
    unittest.main()
