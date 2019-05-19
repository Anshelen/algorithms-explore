"""
Задача о лестнице. Дана лестница и целые числа , которыми помечены ступеньки.
Найдите максимальную сумму, которую можно получить, идя по лестнице снизу вверх
(от нулевой до n-й ступеньки), каждый раз поднимаясь на одну или две ступеньки.
Сложность алгоритма O(n).
"""

from typing import List


def count_recursive(lst: List[int]):
    """
    Подсчет максимальной суммы рекурсивно (методом сверху вниз).
    """
    if not lst:
        return 0
    if len(lst) == 1:
        return lst[0]
    d = {}

    def _count(i):
        if i not in d:
            if i != len(lst) - 1:
                a = _count(i + 1) + lst[i]
                if i + 2 <= len(lst) - 1:
                    b = _count(i + 2) + lst[i]
                    d[i] = max(a, b)
                else:
                    d[i] = a
            else:
                d[i] = lst[i]
        return d[i]
    return max(_count(0), _count(1))


def count_iterative(lst: List[int]):
    """
    Подсчет максимальной суммы итеративно (методом снизу вверх).
    """
    if not lst:
        return 0
    if len(lst) == 1:
        return lst[0]
    d = [lst[0], lst[0] + lst[1] if lst[0] > 0 else lst[1]]
    for i in range(2, len(lst)):
        d.append(max(d[i - 1], d[i - 2]) + lst[i])
    return d[len(lst) - 1]


def count_without_list(lst: List[int]):
    """
    Подсчет максимальной суммы без вспомогательного массива.
    """
    if not lst:
        return 0
    if len(lst) == 1:
        return lst[0]
    a, b = lst[0], lst[0] + lst[1] if lst[0] > 0 else lst[1]
    for i in range(2, len(lst)):
        a, b = b, max(a, b) + lst[i]
    return b


if __name__ == '__main__':
    for func in [count_recursive, count_iterative, count_without_list]:
        assert func([]) == 0
        assert func([-1]) == -1
        assert func([-1, 2]) == 2
        assert func([1, 2]) == 3
        assert func([1, 2, 2]) == 5
        assert func([2, -1]) == 1
        assert func([-1, 2, 1]) == 3
