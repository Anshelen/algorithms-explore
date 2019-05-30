"""
Модификация стека, позволяющая получить максимальный элемент за константное
время. Потребляет в два раза больше памяти, чем обычный стек.
"""

import unittest
from typing import Any

from structures.stack import Stack


class MaxStack(Stack):

    def __init__(self) -> None:
        super().__init__()
        self.max_stack = Stack()

    def peek(self):
        return super().peek()

    def push(self, item: Any):
        if self.max_stack.empty():
            self.max_stack.push(item)
        else:
            self.max_stack.push(max(item, self.max_stack.peek()))
        super().push(item)

    def pop(self):
        self.max_stack.pop()
        return super().pop()

    def max(self):
        """
        Получить максимальный элемент. Не извлекает его из стека.
        """
        return self.max_stack.peek()

    def empty(self):
        return super().empty()

    def __len__(self):
        return super().__len__()

    def __bool__(self):
        return super().__bool__()


class MaxStackTests(unittest.TestCase):

    def setUp(self):
        self.stack = MaxStack()

    def test_max_empty(self):
        with self.assertRaises(RuntimeError):
            self.stack.max()

    def test_max_one_operation(self):
        self.stack.push(1)
        self.assertEqual(self.stack.max(), 1)
        self.assertEqual(len(self.stack), 1)

    def test_max_few_operations(self):
        self.stack.push(2)
        self.stack.push(1)
        self.assertEqual(self.stack.max(), 2)
        self.stack.push(4)
        self.assertEqual(self.stack.max(), 4)


if __name__ == '__main__':
    unittest.main()
