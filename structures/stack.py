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
        self._size = 0

    def peek(self):
        if self.empty():
            raise RuntimeError('Stack is empty')
        return self._head.value

    def pop(self):
        if self.empty():
            raise RuntimeError('Stack is empty')
        res = self._head.value
        self._head = self._head.next
        self._size -= 1
        return res

    def push(self, item):
        new_node = _Node(item, self._head if not self.empty() else None)
        self._head = new_node
        self._size += 1

    def empty(self):
        return self._head is None

    def __bool__(self):
        return not self.empty()

    def __len__(self):
        return self._size


class StackTest(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_empty(self):
        self.assertTrue(self.stack.empty())

    def test_not_empty(self):
        self.stack.push(1)
        self.assertFalse(self.stack.empty())

    def test_push_first(self):
        self.stack.push(1)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_empty(self):
        with self.assertRaises(RuntimeError):
            self.stack.pop()

    def test_push_and_pop(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.stack.push(3)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 1)
        self.stack.push(4)
        self.assertEqual(self.stack.pop(), 4)

    def test_peek_empty(self):
        with self.assertRaises(RuntimeError):
            self.stack.peek()

    def test_peek_not_empty(self):
        self.stack.push(1)
        self.assertEqual(self.stack.peek(), 1)
        self.assertEqual(len(self.stack), 1)

    def test_bool_empty(self):
        self.assertFalse(self.stack)

    def test_bool_not_empty(self):
        self.stack.push(0)
        self.assertTrue(self.stack)

    def test_len(self):
        self.stack.push(0)
        self.assertEqual(len(self.stack), 1)


if __name__ == '__main__':
    unittest.main()
