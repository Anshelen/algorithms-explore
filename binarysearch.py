"""
Алгоритм двоичного поиска.
"""

from typing import Sequence, TypeVar, List


Element = TypeVar("Element")


def search(lst: Sequence[Element], el: Element) -> int:
    """
    Ищет индекс вхождения элемента в упорядоченном массиве. Если элемента нет,
    то возвращает -1. Сложность O(log n).
    """
    left, right = 0, len(lst) - 1
    while left <= right:
        m = (left + right) // 2
        if lst[m] == el:
            return m
        elif lst[m] > el:
            right = m - 1
        else:
            left = m + 1
    return -1


def index(lst: List[Element], el: Element) -> int:
    """
    Возвращает такой индекс i в массиве A, что A[i-1] <= el <= A[i+1]. То есть
    с помощью бинарного поиска находит позицию, в которую элемент мог бы быть
    помещен, при этом не нарушив сортировки. Сложность O(log n).
    """
    if not lst:
        return 0
    left, right, m = 0, len(lst) - 1, 0
    while left <= right:
        m = (left + right) // 2
        if lst[m] == el:
            return m
        elif lst[m] > el:
            right = m - 1
        else:
            left = m + 1
    return m if lst[m] > el else m + 1


if __name__ == '__main__':

    assert search([], 1) == -1
    assert search([1], 1) == 0
    assert search([1], 2) == -1
    assert search([1, 1], 2) == -1
    assert search([1, 1], 1) == 0
    assert search([1, 0, 1], 1) == 2
    assert search([1, 2, 3], 2) == 1
    assert search([1, 2, 3], 4) == -1
    assert search([1, 1, 2], 1) == 1
    assert search([1, 1, 2, 2], 1) == 1
    assert search([1, 1, 1, 2], 1) == 1
    assert search([1, 2, 3, 4, 5, 6, 6, 6, 7], 2) == 1
    assert search([1, 2, 3, 4, 5, 6, 6, 6, 7], 4) == 3
    assert search([1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 7], 6) == 8
    assert search([1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 7], 7) == 11
    assert search([1, 2, 3, 4, 5, 5, 5, 5, 6, 6, 6, 7], 1) == 0

    assert index([], 1) == 0
    assert index([1], 1) == 0
    assert index([2], 1) == 0
    assert index([0], 1) == 1
    assert index([0, 2, 3], 1) == 1
    assert index([0, 2, 3], 2) == 1
    assert index([0, 1, 2, 3], 1) == 1
    assert index([0, 1, 2, 3], 4) == 4
    assert index([0, 1, 2, 3], 0) == 0
