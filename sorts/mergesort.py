"""
Алгоритм сортировуи слиянием. Сложность О(n*log n).
"""

from typing import List


def merge_sort_recursive(lst: List):
    """
    Сортировка слиянием, реализованная с помощью рекурсии.
    Требует O(n) дополнительной памяти (для слияния массивов).
    """
    if len(lst) <= 1:
        return lst
    m = len(lst) // 2
    return _merge(merge_sort_recursive(lst[:m]), merge_sort_recursive(lst[m:]))


def merge_sort_iterative(lst: List):
    """
    Сортировка слиянием, реализованная с помощью очереди.
    Требует O(n) дополнительной памяти (для слияния массивов).
    """
    if not lst:
        return lst
    lst = [[el] for el in lst]
    while len(lst) > 1:
        lst.append(_merge(lst.pop(0), lst.pop(0)))
    return lst.pop(0)


def _merge(a: List, b: List):
    """ Сливает два упорядоченных списка в один. """
    i, j, res = 0, 0, []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    res.extend(a[i:])
    res.extend(b[j:])
    return res


if __name__ == '__main__':

    for func in [merge_sort_iterative, merge_sort_recursive]:
        assert func([]) == []
        assert func([1]) == [1]
        assert func([1, 2]) == [1, 2]
        assert func([2, 1]) == [1, 2]
        assert func([2, 1, 3]) == [1, 2, 3]
        assert func([2, 1, 4, 3, 3, 5]) == [1, 2, 3, 3, 4, 5]
        assert func([5, 3, 2, 3, 1, 4]) == [1, 2, 3, 3, 4, 5]
        assert func([3, 3, 2, 1, 4, 5]) == [1, 2, 3, 3, 4, 5]
        assert func([3, 3, 2, 1, 6, 4, 5]) == [1, 2, 3, 3, 4, 5, 6]
