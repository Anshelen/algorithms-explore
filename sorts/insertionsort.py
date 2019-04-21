"""
Алгоритм сортировки вставками. Сложность О(n^2).
"""

from typing import List


def insertion_sort(lst: List):
    """
    Сортировка вставками.
    """
    for i in range(1, len(lst)):
        j = i
        while j > 0:
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
                j -= 1
            else:
                break
    return lst


if __name__ == '__main__':

    assert insertion_sort([]) == []
    assert insertion_sort([1]) == [1]
    assert insertion_sort([1, 2]) == [1, 2]
    assert insertion_sort([2, 1]) == [1, 2]
    assert insertion_sort([2, 1, 3]) == [1, 2, 3]
    assert insertion_sort([2, 1, 4, 3, 3, 5]) == [1, 2, 3, 3, 4, 5]
    assert insertion_sort([5, 3, 2, 3, 1, 4]) == [1, 2, 3, 3, 4, 5]
    assert insertion_sort([3, 3, 2, 1, 4, 5]) == [1, 2, 3, 3, 4, 5]
    assert insertion_sort([3, 3, 2, 1, 6, 4, 5]) == [1, 2, 3, 3, 4, 5, 6]
