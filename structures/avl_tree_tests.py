import math
import random
import unittest
from abc import ABC

from structures.avl_tree import TreeMap


class TreeMapTests(ABC):

    def setUp(self):
        self.map = TreeMap[int, int]()

    def fill(self, arr, tree=None):
        if tree is None:
            tree = self.map
        for x in arr:
            if type(x) is tuple:
                k, v = x
            else:
                k, v = x, x
            tree[k] = v

    def validate_tree(self, tree=None):
        if tree is None:
            tree = self.map
        root = tree.root
        if root is None:
            return
        self.assertIsNone(root.parent)

        # Возвращает минимальное и максимальное значение в поддереве
        def __validate(node):
            left_height, right_height = 0, 0
            left_size, right_size = 0, 0
            l_min, r_max = math.inf, -1 * math.inf
            if node.left:
                self.assertEqual(node.left.parent, node)
                l_min, l_max = __validate(node.left)
                self.assertLess(l_max, node.key)
                left_height = node.left.height
                left_size = node.left.size
            if node.right:
                self.assertEqual(node.right.parent, node)
                r_min, r_max = __validate(node.right)
                self.assertGreater(r_min, node.key)
                right_height = node.right.height
                right_size = node.right.size
            self.assertTrue(abs(left_height - right_height) <= 1)
            self.assertEqual(node.height, max(left_height, right_height) + 1)
            self.assertEqual(node.size, left_size + right_size + 1)
            return min(node.key, l_min), max(node.key, r_max)
        __validate(root)


class PutAndGetTests(TreeMapTests, unittest.TestCase):

    def test_put_and_get(self):
        self.fill([1, 2])
        self.assertEqual(self.map[1], 1)
        self.assertEqual(self.map[2], 2)

    def test_put_and_get_same_key(self):
        self.fill([1, 2, (1, 3)])
        self.assertEqual(self.map[1], 3)
        self.map[2] = 4
        self.assertEqual(self.map[2], 4)

    def test_get_empty(self):
        with self.assertRaises(KeyError):
            self.map[1]

    def test_get_not_containing(self):
        self.map[1] = 1
        with self.assertRaises(KeyError):
            self.map[2]

    def test_put_and_get_dynamic(self):
        for i in range(150):
            el = random.randint(0, 20)
            self.map[el] = el
            self.assertEqual(self.map[el], el)
            self.validate_tree()


class DeleteTests(TreeMapTests, unittest.TestCase):

    def test_delete_root_no_children(self):
        self.map[1] = 1
        del self.map[1]
        with self.assertRaises(KeyError):
            self.map[1]

    def test_delete_root_one_child(self):
        self.fill([1, 2])
        del self.map[1]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[1]

    def test_delete_root_two_children(self):
        self.fill([1, 2, 0])
        del self.map[1]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[1]

    def test_delete_leaf(self):
        self.fill([1, 2])
        del self.map[2]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[2]

    def test_delete_one_child_right_subtree(self):
        self.fill([1, 2, 3])
        del self.map[2]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[2]

    def test_delete_one_child_left_subtree(self):
        self.fill([1, 2, 1.5])
        del self.map[2]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[2]

    def test_delete_two_children(self):
        self.fill([1, 2, 3, 1.5])
        del self.map[2]
        self.validate_tree()
        with self.assertRaises(KeyError):
            self.map[2]

    def test_delete_empty(self):
        with self.assertRaises(KeyError):
            del self.map[1]

    def test_delete_not_containing(self):
        self.map[1] = 1
        with self.assertRaises(KeyError):
            del self.map[2]

    def test_delete_dynamic(self):
        keys = [i for i in range(150)]
        random.shuffle(keys)
        self.fill(keys)
        random.shuffle(keys)
        for k in keys:
            self.validate_tree()
            del self.map[k]
            with self.assertRaises(KeyError):
                self.map[k]


class FindMaxMinTests(TreeMapTests, unittest.TestCase):

    def test_find_max_key_value(self):
        self.fill([1, 3, 2])
        self.assertEqual(self.map.max_key_value(), 3)

    def test_find_max_key_value_empty(self):
        with self.assertRaises(RuntimeError):
            self.map.max_key_value()

    def test_find_min_key_value(self):
        self.fill([1, 3, 0, 2])
        self.assertEqual(self.map.min_key_value(), 0)

    def test_find_min_key_value_empty(self):
        with self.assertRaises(RuntimeError):
            self.map.min_key_value()

    def test_min_and_max_key_value_dynamic(self):
        keys = [random.randint(0, 100) for _ in range(150)]
        random.shuffle(keys)
        self.fill(keys)
        self.assertEqual(self.map.max_key_value(), max(keys))
        self.assertEqual(self.map.min_key_value(), min(keys))


class FindNextPrevKeyValueTests(TreeMapTests, unittest.TestCase):

    def test_find_next_key_value_has_right(self):
        self.fill([1, 3, 0, 2, 5])
        self.assertEqual(self.map.next_key_value(3), 5)

    def test_find_next_key_value_move_up(self):
        self.fill([1, 3, 0, 2, 5, 2.5])
        self.assertEqual(self.map.next_key_value(2.5), 3)

    def test_find_next_key_value_no_next(self):
        self.fill([1, 3, 0, 2, 5])
        self.assertIsNone(self.map.next_key_value(5))

    def test_find_next_key_value_empty(self):
        with self.assertRaises(KeyError):
            self.map.next_key_value(3)

    def test_find_next_key_value_not_contains(self):
        self.map[3] = 3
        with self.assertRaises(KeyError):
            self.map.next_key_value(1)

    def test_find_prev_key_value_has_left(self):
        self.fill([1, 3, 0, 2, 5])
        self.assertEqual(self.map.prev_key_value(3), 2)

    def test_find_prev_key_value_move_up(self):
        self.fill([1, 3, 0, 2, 5, 4])
        self.assertEqual(self.map.prev_key_value(4), 3)

    def test_find_prev_key_value_no_prev(self):
        self.fill([1, 3, 0, 2, 5])
        self.assertIsNone(self.map.prev_key_value(0))

    def test_find_prev_key_value_empty(self):
        with self.assertRaises(KeyError):
            self.map.prev_key_value(3)

    def test_find_prev_key_value_not_contains(self):
        self.map[3] = 3
        with self.assertRaises(KeyError):
            self.map.prev_key_value(1)

    def test_next_and_prev_key_value_dynamic(self):
        keys = [i for i in range(150)]
        random.shuffle(keys)
        self.fill(keys)
        keys.sort()
        for i in range(len(keys) - 1):
            self.assertEqual(self.map.next_key_value(keys[i]), keys[i + 1])
            self.assertEqual(self.map.prev_key_value(keys[i + 1]), keys[i])
        self.assertIsNone(self.map.next_key_value(keys[len(keys) - 1]))
        self.assertIsNone(self.map.prev_key_value(keys[0]))


class LenAndBoolAndContainTests(TreeMapTests, unittest.TestCase):

    def test_empty(self):
        self.assertEqual(len(self.map), 0)
        self.assertFalse(self.map)
        self.assertFalse(0 in self.map)

    def test_after_put(self):
        self.map[1] = 1
        self.assertEqual(len(self.map), 1)
        self.assertTrue(self.map)
        self.assertTrue(1 in self.map)

    def test_after_put_same_key_elements(self):
        self.fill([1, (1, 3)])
        self.assertEqual(len(self.map), 1)
        self.assertTrue(self.map)
        self.assertTrue(1 in self.map)

    def test_after_deleting(self):
        self.map[1] = 1
        del self.map[1]
        self.assertEqual(len(self.map), 0)
        self.assertFalse(self.map)
        self.assertFalse(1 in self.map)


class GetByIndexTests(TreeMapTests, unittest.TestCase):

    def test_empty(self):
        with self.assertRaises(IndexError):
            self.map.get_by_index(0)

    def test_overflow_index(self):
        self.map[1] = 2
        with self.assertRaises(IndexError):
            self.map.get_by_index(1)

    def test_negative_index(self):
        self.map[1] = 2
        with self.assertRaises(IndexError):
            self.map.get_by_index(-1)

    def test_common(self):
        self.fill([1, 0, 3])
        self.assertEqual(self.map.get_by_index(0), 0)
        self.assertEqual(self.map.get_by_index(1), 1)
        self.assertEqual(self.map.get_by_index(2), 3)

    def test_after_delete(self):
        self.fill([1, 0, 3])
        del self.map[1]
        self.assertEqual(self.map.get_by_index(1), 3)

    def test_dynamic(self):
        keys = [i for i in range(150)]
        random.shuffle(keys)
        self.fill(keys)
        keys.sort()
        for i in range(len(keys)):
            self.assertEqual(self.map.get_by_index(i), keys[i])


class MergeTests(TreeMapTests, unittest.TestCase):

    def assertContains(self, arr):
        s_arr = sorted(arr)
        self.assertEqual(len(self.map), len(arr))
        for i in range(len(arr)):
            self.assertEqual(self.map.get_by_index(i), s_arr[i])

    def setUp(self):
        self.map = TreeMap()
        self.map2 = TreeMap()

    def launch_test(self, arr1, arr2):
        self.fill(arr1)
        self.fill(arr2, tree=self.map2)
        self.map.merge(self.map2)
        self.assertContains(arr1 + arr2)
        self.validate_tree()

    def test_empty_first(self):
        self.launch_test([1, 2], [])

    def test_empty_second(self):
        self.launch_test([], [1, 2])

    def test_empty_both(self):
        self.launch_test([], [])

    def test_equal_height(self):
        self.launch_test([1, 2, 0, 4, 3], [5, 7, 8, 6, 9])

    def test_first_height_more(self):
        self.launch_test([1, 2, 0, 4, 3], [5, 6])

    def test_second_height_more(self):
        self.launch_test([1, 2, 0], [3, 5, 7, 8, 6, 4])

    def test_one_element_in_first_tree(self):
        self.launch_test([1], [2, 3, 5])

    def test_one_element_in_second_tree(self):
        self.launch_test([1, 2], [5])

    def test_right_tree_higher(self):
        self.launch_test([0, 1], [50, 51, 52, 53])

    def test_middle_element_has_one_child(self):
        self.launch_test([1, 0, 3, 2], [5, 6, 7])

    def test_dynamic(self):
        for _ in range(50):
            self.setUp()
            map_size, map2_size = random.randint(1, 50), random.randint(1, 50)
            arr1 = [i for i in range(map_size)]
            arr2 = [i + 50 for i in range(map2_size)]
            self.launch_test(arr1, arr2)


class SplitTests(TreeMapTests, unittest.TestCase):

    def launch_test(self, arr, key):
        self.fill(arr)
        a, b = self.map.split(key)
        self.validate_tree(tree=a)
        self.validate_tree(tree=b)
        self.assertEqual(len(set(arr)), len(a) + len(b))
        for i in range(len(a)):
            self.assertLessEqual(a.get_by_index(i), key)
        for i in range(len(b)):
            self.assertGreater(b.get_by_index(i), key)

    def test_middle(self):
        self.launch_test([1, 0, 2, 6, 3, -1], 3)

    def test_root(self):
        self.launch_test([1, 0, 2, 6, 3, -1], 1)

    def test_leaf(self):
        self.launch_test([1, 0, 2, 6, 3, -1], 2)

    def test_not_contained_key(self):
        self.launch_test([1, 0, 2, 6, 3, -1], 4)

    def test_less_then_minimum(self):
        self.launch_test([1, 0, 2, 6, 3, -1], -10)

    def test_more_then_maximum(self):
        self.launch_test([1, 0, 2, 6, 3, -1], 10)

    def test_empty(self):
        self.launch_test([], 10)

    def test_dynamic(self):
        for _ in range(150):
            self.setUp()
            arr = [random.randint(0, 50) for _ in range(25)]
            div = random.randint(0, 50)
            self.launch_test(arr, div)


if __name__ == '__main__':
    unittest.main()
