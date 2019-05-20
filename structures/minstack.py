"""
Модификация стека, позволяющая получить минимальный элемент за константное
время. Потребляет в два раза больше памяти, чем обычный стек.
"""

import queue
import unittest
from typing import Optional


class MinStack(queue.LifoQueue):

    def _init(self, maxsize: int) -> None:
        super()._init(maxsize)
        self.min_stack = queue.LifoQueue()

    def _put(self, item):
        if self.min_stack.empty():
            self.min_stack.put(item)
        else:
            min_el = self.min_stack.get()
            self.min_stack.put(min_el)
            self.min_stack.put(min(item, min_el))
        super()._put(item)

    def _get(self):
        self.min_stack.get()
        return super()._get()

    def get_min(self, block: bool = True, timeout: Optional[float] = None):
        """
        Получить минимальный элемент. Не извлекает его из стека. Аргументы block
        и timeout аналогичны присутствующим в методе LifoQueue.get().
        """
        res = self.min_stack.get(block, timeout)
        self.min_stack.put(res)
        return res


class MinStackTests(unittest.TestCase):

    def setUp(self):
        self.stack = MinStack()

    def test_put(self):
        self.stack.put(1)
        self.assertEqual(self.stack.queue, [1])
        self.assertEqual(self.stack.min_stack.queue, [1])

    def test_get(self):
        self.stack.put(1)
        self.assertEqual(self.stack.get(), 1)
        self.assertEqual(self.stack.min_stack.queue, [])

    def test_get_min_first_operation(self):
        self.stack.put(1)
        self.assertEqual(self.stack.get_min(), 1)
        self.assertEqual(self.stack.queue, [1])
        self.assertEqual(self.stack.min_stack.queue, [1])

    def test_get_min_few_operations(self):
        self.stack.put(2)
        self.stack.put(1)
        self.stack.put(4)
        self.assertEqual(self.stack.get_min(), 1)
        self.assertEqual(self.stack.queue, [2, 1, 4])
        self.assertEqual(self.stack.min_stack.queue, [2, 1, 1])


if __name__ == '__main__':
    unittest.main()
