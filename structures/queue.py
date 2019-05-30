"""
Реализация очереди на основе односвязанного списка.
"""

import unittest
from typing import Any, Optional


class Queue:
    class Node:
        def __init__(self, value: Any, nxt: Optional['Queue.Node']) -> None:
            self.value = value
            self.next: Optional['Queue.Node'] = nxt

    def __init__(self) -> None:
        self._head: Queue.Node = None
        self._tail: Queue.Node = None
        self._size = 0

    def peek(self) -> Any:
        if self.empty():
            raise RuntimeError('Queue is empty')
        return self._head.value

    def pop(self) -> Any:
        if self.empty():
            raise RuntimeError('Queue is empty')
        res = self._head.value
        self._head = self._head.next
        self._size -= 1
        return res

    def push(self, item: Any) -> None:
        new_node = Queue.Node(item, None)
        if not self.empty():
            self._tail.next = new_node
        else:
            self._head = new_node
        self._tail = new_node
        self._size += 1

    def empty(self) -> bool:
        return self._head is None

    def __len__(self):
        return self._size

    def __bool__(self):
        return not self.empty()


class QueueTest(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

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


if __name__ == '__main__':
    unittest.main()
