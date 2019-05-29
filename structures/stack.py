"""
Реализация стека на основе односвязанного списка.
"""

import unittest
from collections import namedtuple


class _Node(namedtuple('_Node', ['value', 'next'])):
    pass


class Stack:

    def __init__(self) -> None:
        self._head = None

    def get(self):
        if self.empty():
            raise RuntimeError('Stack is empty')
        res = self._head.value
        self._head = self._head.next
        return res

    def put(self, item):
        new_node = _Node(item, self._head if not self.empty() else None)
        self._head = new_node

    def empty(self):
        return self._head is None

    def __bool__(self):
        return not self.empty()


class StackTest(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_empty(self):
        self.assertTrue(self.stack.empty())

    def test_not_empty(self):
        self.stack.put(1)
        self.assertFalse(self.stack.empty())

    def test_put_first(self):
        self.stack.put(1)
        self.assertEqual(self.stack.get(), 1)

    def test_get_empty(self):
        with self.assertRaises(RuntimeError):
            self.stack.get()

    def test_common(self):
        self.stack.put(1)
        self.stack.put(2)
        self.assertEqual(self.stack.get(), 2)
        self.stack.put(3)
        self.assertEqual(self.stack.get(), 3)
        self.assertEqual(self.stack.get(), 1)
        self.stack.put(4)
        self.assertEqual(self.stack.get(), 4)

    def test_bool_empty(self):
        self.assertFalse(self.stack)

    def test_bool_not_empty(self):
        self.stack.put(0)
        self.assertTrue(self.stack)


if __name__ == '__main__':
    unittest.main()
