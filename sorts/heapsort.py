"""
Сортировка кучей (пирамидальная сортировка). Сложность О(n*log n).
Сортирует на месте.
"""

from structures.heap import Heap


class SortingHeap(Heap):
    """
    Макс-куча, позволяющая отсортировать внутренний массив, тем самым упорядочив
    его по возрастанию.
    """

    def __init__(self, lst=None, prior_func=lambda x: -x):
        self.size = len(lst) - 1
        super().__init__(lst, prior_func)

    def _has_left_child(self, index):
        left_child_index = 2 * index + 1
        return left_child_index <= self.size

    def _has_right_child(self, index):
        right_child_index = 2 * index + 2
        return right_child_index <= self.size

    def sort(self):
        while self.size > 0:
            self[0], self[self.size] = self[self.size], self[0]
            self.size -= 1
            self._shift_down(0)


def heapsort(lst):
    SortingHeap(lst).sort()
