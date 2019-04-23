"""
Подсчет количества инверсий в массиве. Инверсия - это пара индексов 1≤i<j≤n,
для которых A[i]>A[j]. (Количество инверсий в массиве является в некотором
смысле его мерой неупорядоченности: например, в упорядоченном по неубыванию
массиве инверсий нет вообще, а в массиве, упорядоченном по убыванию, инверсию
образуют каждые два элемента.)
"""

from typing import List


def count_inversions_naive(lst: List):
    """
    Считает количество инверсий. Сложность алгоритма О(n^2).
    """
    inv = 0
    for i in range(1, len(lst)):
        for j in range(i):
            if lst[j] > lst[i]:
                inv += 1
    return inv


def count_inversions_with_merge(lst: List):
    """
    Считает количество инверсий. Алгоритм основан на сортировке слиянием.
    Следовательно сложность алгоритма О(n*log n).
    """
    inv = 0

    def merge_and_count(x: List):
        """ Рекурсивно осуществляет сортировку слиянием и подсчитывает
        количество инверсий."""
        if len(x) <= 1:
            return x
        m = len(x) // 2
        return _merge(merge_and_count(x[:m]), merge_and_count(x[m:]))

    def _merge(a: List, b: List):
        """ Сливает два упорядоченных списка в один. """
        i, j, res = 0, 0, []
        nonlocal inv
        while i < len(a) and j < len(b):
            if a[i] > b[j]:
                inv += len(a) - i
                res.append(b[j])
                j += 1
            else:
                res.append(a[i])
                i += 1
        res.extend(a[i:])
        res.extend(b[j:])
        return res

    merge_and_count(lst[:])
    return inv


if __name__ == '__main__':

    for func in [count_inversions_naive, count_inversions_with_merge]:
        assert func([]) == 0
        assert func([1]) == 0
        assert func([1, 1]) == 0
        assert func([1, 2]) == 0
        assert func([2, 1]) == 1
        assert func([1, 1, 2]) == 0
        assert func([2, 1, 1]) == 2
        assert func([3, 2, 1]) == 3
        assert func([2, 3, 1]) == 2
        assert func([4, 3, 2, 1]) == 6
        assert func([2, 3, 9, 2, 9]) == 2
