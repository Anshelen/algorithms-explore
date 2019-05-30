"""
Модификация очереди, позволяющая получить максимальный элемент время. Все
операции делает в среднем за константное время. Построена на базе двух стеков.
Потребляет в два раза больше памяти, чем обычная очередь.
"""

import math
import unittest
from typing import Any

from structures.max_stack import MaxStack


class MaxQueue:

    def __init__(self):
        self.left = MaxStack()
        self.right = MaxStack()

    def push(self, item: Any):
        self.left.push(item)

    def peek(self):
        if self.right.empty():
            self._move_items_right()
        if self.right.empty():
            raise RuntimeError('Queue is empty')
        return self.right.peek()

    def pop(self):
        if self.right.empty():
            self._move_items_right()
        if self.right.empty():
            raise RuntimeError('Queue is empty')
        return self.right.pop()

    def max(self):
        """
        Получить максимальный элемент. Не извлекает его из очереди.
        """
        if self.left.empty() and self.right.empty():
            raise RuntimeError('Queue is empty')
        else:
            a = self.left.max() if self.left else -1 * math.inf
            b = self.right.max() if self.right else -1 * math.inf
            return max(a, b)

    def empty(self):
        return self.left.empty() and self.right.empty()

    def __len__(self):
        return len(self.left) + len(self.right)

    def __bool__(self):
        return not self.empty()

    def _move_items_right(self):
        while not self.left.empty():
            self.right.push(self.left.pop())


class MaxStackTests(unittest.TestCase):

    def setUp(self):
        self.queue = MaxQueue()

    def test_empty(self):
        self.assertTrue(self.queue.empty())

    def test_not_empty(self):
        self.queue.push(1)
        self.assertFalse(self.queue.empty())

    def test_pop_empty(self):
        with self.assertRaises(RuntimeError):
            self.queue.pop()

    def test_peek_empty(self):
        with self.assertRaises(RuntimeError):
            self.queue.peek()

    def test_peek_not_empty(self):
        self.queue.push(1)
        self.assertEqual(self.queue.peek(), 1)
        self.assertEqual(len(self.queue), 1)

    def test_push_and_pop_once(self):
        self.queue.push(1)
        self.assertEqual(self.queue.pop(), 1)

    def test_push_and_pop(self):
        self.queue.push(1)
        self.queue.push(2)
        self.assertEqual(self.queue.pop(), 1)
        self.queue.push(3)
        self.assertEqual(self.queue.pop(), 2)
        self.assertEqual(self.queue.pop(), 3)
        self.queue.push(4)
        self.assertEqual(self.queue.pop(), 4)

    def test_bool_empty(self):
        self.assertFalse(self.queue)

    def test_bool_not_empty(self):
        self.queue.push(0)
        self.assertTrue(self.queue)

    def test_zero_size(self):
        self.assertEqual(len(self.queue), 0)

    def test_non_zero_size(self):
        self.queue.push(0)
        self.queue.push(1)
        self.queue.pop()
        self.assertEqual(len(self.queue), 1)

    def test_max_empty(self):
        with self.assertRaises(RuntimeError):
            self.queue.max()

    def test_size_not_changed_using_max(self):
        self.queue.push(1)
        self.assertEqual(self.queue.max(), 1)
        self.assertEqual(len(self.queue), 1)

    def test_max(self):
        self.queue.push(2)
        self.assertEqual(self.queue.max(), 2)
        self.queue.push(1)
        self.assertEqual(self.queue.max(), 2)
        self.queue.push(3)
        self.assertEqual(self.queue.max(), 3)
        self.queue.pop()
        self.assertEqual(self.queue.max(), 3)


if __name__ == '__main__':
    unittest.main()
