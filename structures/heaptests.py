import random
import unittest
from abc import ABC

from structures.heap import Heap


class AbstractHeapTest(ABC, unittest.TestCase):

    def setUp(self):
        self.heap = Heap()

    def verify_heap(self):
        if not self.heap:
            return
        func = self.heap.prior_func
        for index in range(1, len(self.heap)):
            current = self.heap[index]
            parent = self.heap[(index - 1) // 2]
            self.assertGreaterEqual(func(current), func(parent))

    def assertHeapState(self, target):
        self.assertEqual(target, self.heap.lst)

    def setHeapState(self, target):
        self.heap.lst = target


class VerifyHeapTests(AbstractHeapTest):

    def test_verify_ok(self):
        self.setHeapState([1, 2, 3, 3, 4, 5, 5])
        self.verify_heap()

    def test_verify_empty_heap(self):
        self.setHeapState([])
        self.verify_heap()

    def test_verify_all_same_elements(self):
        self.setHeapState([1, 1, 1])
        self.verify_heap()

    @unittest.expectedFailure
    def test_verify_invalid_heap_state(self):
        self.setHeapState([5, 2, 3, 4])
        self.verify_heap()

    @unittest.expectedFailure
    def test_verify_invalid_heap_state_with_same_elements(self):
        self.setHeapState([1, 3, 3, 2])
        self.verify_heap()


class InitHeapTests(AbstractHeapTest):

    def test_empty(self):
        self.heap = Heap(lst=[])
        self.verify_heap()

    def test_dynamic(self):
        for i in range(100):
            lst = [random.randint(0, 100) for _ in range(50)]
            self.heap = Heap(lst=lst)
            self.verify_heap()


class ShiftUpTests(AbstractHeapTest):

    def test_no_need_to_shift_up_first_element(self):
        self.setHeapState([1, 2, 3])
        self.heap._shift_up(0)
        self.assertHeapState([1, 2, 3])

    def test_no_need_to_shift_up_middle_element(self):
        self.setHeapState([1, 2, 3])
        self.heap._shift_up(1)
        self.assertHeapState([1, 2, 3])

    def test_no_need_to_shift_up_equal_elements(self):
        self.setHeapState([1, 2, 3, 2])
        self.heap._shift_up(3)
        self.assertHeapState([1, 2, 3, 2])

    def test_shift_up_middle_element(self):
        self.setHeapState([1, 2, 3, 1, 4, 4, 5])
        self.heap._shift_up(3)
        self.assertHeapState([1, 1, 3, 2, 4, 4, 5])

    def test_shift_up_last_element(self):
        self.setHeapState([1, 2, 3, 1])
        self.heap._shift_up(3)
        self.assertHeapState([1, 1, 3, 2])


class ShiftDownTests(AbstractHeapTest):

    def test_no_need_to_shift_down_leaf(self):
        self.setHeapState([1, 2, 3, 4])
        self.heap._shift_down(3)
        self.assertHeapState([1, 2, 3, 4])

    def test_no_need_to_shift_down_one_child(self):
        self.setHeapState([1, 2, 3, 4])
        self.heap._shift_down(1)
        self.assertHeapState([1, 2, 3, 4])

    def test_no_need_to_shift_down_two_children(self):
        self.setHeapState([1, 2, 3, 4, 5])
        self.heap._shift_down(1)
        self.assertHeapState([1, 2, 3, 4, 5])

    def test_no_need_to_shift_down_one_equal_child(self):
        self.setHeapState([1, 2, 3, 2, 4])
        self.heap._shift_down(1)
        self.assertHeapState([1, 2, 3, 2, 4])

    def test_no_need_to_shift_down_two_equal_children(self):
        self.setHeapState([1, 2, 3, 2, 2])
        self.heap._shift_down(1)
        self.assertHeapState([1, 2, 3, 2, 2])

    def test_shift_down_first_element(self):
        self.setHeapState([5, 1, 3, 4, 2])
        self.heap._shift_down(0)
        self.assertHeapState([1, 2, 3, 4, 5])

    def test_shift_down_middle_element(self):
        self.setHeapState([1, 5, 3, 7, 2, 3])
        self.heap._shift_down(1)
        self.assertHeapState([1, 2, 3, 7, 5, 3])

    def test_shift_down_with_priority_function(self):
        self.heap = Heap(prior_func=lambda x: x[1])
        self.setHeapState([('d', 1), ('c', 2), ('b', 3), ('a', 4)])
        self.heap._shift_down(1)
        self.assertHeapState([('d', 1), ('c', 2), ('b', 3), ('a', 4)])


class InsertTests(AbstractHeapTest):

    def test_insert_in_empty_heap(self):
        self.setHeapState([])
        self.heap.insert(1)
        self.assertHeapState([1])

    def test_insert_minimum_element(self):
        self.setHeapState([1, 2, 3, 4, 5, 5])
        self.heap.insert(0)
        self.assertHeapState([0, 2, 1, 4, 5, 5, 3])

    def test_insert_maximum_element(self):
        self.setHeapState([1, 2, 3, 4, 5, 5])
        self.heap.insert(10)
        self.assertHeapState([1, 2, 3, 4, 5, 5, 10])

    def test_insert_middle_element(self):
        self.setHeapState([1, 2, 3, 4, 5, 5])
        self.heap.insert(2)
        self.assertHeapState([1, 2, 2, 4, 5, 5, 3])

    def test_insert_with_random(self):
        for i in range(100):
            self.heap.insert(random.randint(0, 100))
            self.verify_heap()

    def test_insert_with_random_and_priority_function(self):
        self.heap = Heap(prior_func=lambda x: x[1])
        for i in range(100):
            self.heap.insert(('a', random.randint(0, 100)))
            self.verify_heap()


class ExtendTests(AbstractHeapTest):

    def test_extend_in_empty_heap(self):
        self.setHeapState([])
        self.heap.extend([2, 1, 5, 4, 3])
        self.assertHeapState([1, 2, 5, 4, 3])

    def test_extend_with_empty_array(self):
        self.setHeapState([1, 2, 3])
        self.heap.extend([])
        self.assertHeapState([1, 2, 3])

    def test_extend_common(self):
        self.setHeapState([1, 2, 3])
        self.heap.extend([0, 2, 4])
        self.assertHeapState([0, 1, 3, 2, 2, 4])

    def test_with_random(self):
        for i in range(100):
            size = random.randint(0, 10)
            lst = [random.randint(0, 100) for _ in range(size)]
            self.heap.extend(lst)
            self.verify_heap()

    def test_with_random_and_priority_function(self):
        self.heap = Heap(prior_func=lambda x: x[1])
        for i in range(100):
                size = random.randint(0, 10)
                lst = [('a', random.randint(0, 100)) for _ in range(size)]
                self.heap.extend(lst)
                self.verify_heap()


class IndexTests(AbstractHeapTest):

    def test_common(self):
        self.setHeapState([1, 2, 3])
        self.assertEqual(1, self.heap._index(2))

    def test_index_of_not_contained(self):
        self.setHeapState([1, 2, 3])
        with self.assertRaises(ValueError):
            self.heap._index(4)

    def test_index_of_with_empty_heap(self):
        self.setHeapState([])
        with self.assertRaises(ValueError):
            self.heap._index(4)

    def test_common_with_priority_function(self):
        self.heap = Heap(prior_func=lambda x: x[1])
        self.setHeapState([('a', 1), ('b', 2), ('c', 3)])
        self.assertEqual(1, self.heap._index(('b', 2)))

    def test_common_with_priority_function_and_not_contained(self):
        self.heap = Heap(prior_func=lambda x: x[1])
        self.setHeapState([('a', 1), ('b', 2), ('c', 3)])
        with self.assertRaises(ValueError):
            self.heap._index(('a', 2))


class RemoveTests(AbstractHeapTest):

    def test_remove_min(self):
        self.setHeapState([1, 2, 3])
        self.heap.remove(1)
        self.assertHeapState([2, 3])

    def test_remove_leaf(self):
        self.setHeapState([1, 2, 3, 4])
        self.heap.remove(4)
        self.assertHeapState([1, 2, 3])

    def test_remove_middle_element(self):
        self.setHeapState([1, 2, 3, 4, 5, 6, 7])
        self.heap.remove(2)
        self.assertHeapState([1, 4, 3, 7, 5, 6])

    def test_remove_not_contained(self):
        self.setHeapState([1, 2, 3])
        with self.assertRaises(ValueError):
            self.heap.remove(4)

    def test_remove_from_empty_heap(self):
        self.setHeapState([])
        with self.assertRaises(ValueError):
            self.heap.remove(4)

    def test_with_random(self):
        elements = [random.randint(0, 100) for _ in range(200)]
        self.heap.extend(elements)
        random.shuffle(elements)
        for num in elements:
            self.heap.remove(num)
            self.verify_heap()


class GetMinTests(AbstractHeapTest):

    def test_with_empty_heap(self):
        self.setHeapState([])
        with self.assertRaises(RuntimeError):
            self.heap.get_min()

    def test_common(self):
        self.setHeapState([1, 2, 3])
        self.assertEqual(self.heap.get_min(), 1)
        self.assertHeapState([1, 2, 3])


class ExtractMinTests(AbstractHeapTest):

    def test_with_empty_heap(self):
        self.setHeapState([])
        with self.assertRaises(RuntimeError):
            self.heap.extract_min()

    def test_common(self):
        self.setHeapState([1, 2, 3])
        self.assertEqual(self.heap.extract_min(), 1)
        self.assertHeapState([2, 3])

    def test_with_duplicates(self):
        self.setHeapState([1, 1, 2, 3])
        self.assertEqual(self.heap.extract_min(), 1)
        self.assertHeapState([1, 3, 2])


if __name__ == '__main__':
    unittest.main()
