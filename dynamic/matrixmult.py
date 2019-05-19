"""
Перемножение матриц. Цель определить наименее затратный способ перемножения n
матриц. Стоимость перемножения двух матриц m x n и n x r равна m*n*r. В методы
передается последовательность размеров матриц. Например, для матриц 50x20,
20x1, 1x10, 10x100 аргументы - 50, 20, 1, 10, 100. Сложность алгоритма О(n^3).
"""

import math


def count_recursive(*n: int):
    """
    Считает наименьшую стоимость перемножения матриц рекурсивно (сверху вниз).

    :param n: последовательность размеров матриц
    :return: наименьшая стоимость перемножения матриц
    """
    # Хранит (i, j): cost
    d = {}

    # Считает стоимость перемножения матриц с размерами от m(i) до m(j)
    # включительно. То есть для m = [50, 20, 1, 10, 100] и i = 0, j = 2 -
    # перемножение двух матриц 50x20 и 20x1.
    def _count(i, j):
        if (i, j) not in d:
            if i >= j - 1:
                d[(i, j)] = 0
            else:
                d[(i, j)] = math.inf
                for k in range(i + 1, j):
                    opt = _count(i, k) + _count(k, j) + n[i] * n[k] * n[j]
                    d[(i, j)] = min(d[(i, j)], opt)
        return d[(i, j)]

    return _count(0, len(n) - 1)


def count_iterative(*n: int):
    """
    Считает наименьшую стоимость перемножения матриц итеративно (снизу вверх).

    :param n: последовательность размеров матриц
    :return: наименьшая стоимость перемножения матриц
    """
    if len(n) <= 2:
        return 0
    # Используем только половину матрицы, где j >= i. Наименьшие задачи
    # расположены ближе к основной диагонали, поэтому итерируемся по диагоналям
    d = [[math.inf for _ in n] for _ in n]
    for i in range(len(n)):
        d[i][i] = 0
    for s in range(1, len(n)):
        for i in range(len(n) - s):
            j = i + s
            if i >= j - 1:
                d[i][j] = 0
            for k in range(i + 1, j):
                opt = d[i][k] + d[k][j] + n[i] * n[k] * n[j]
                d[i][j] = min(d[i][j], opt)

    return d[0][len(n) - 1]


def find_recursive(*n: int):
    """
    Возвращает последовательность оптимального перемножения матриц. Действует
    рекурсивным способом (сверху вниз). Последовательность [1, 3, 2] означает,
    что матрицы должны быть перемножены следующим образом ((AxB)x(CxD)).

    :param n: последовательность размеров матриц
    :return: последовательность перемножения матриц
    """
    # Хранит (i, j): (cost, [multiplication order])
    d = {}

    def _find(i, j):
        if (i, j) not in d:
            if i >= j - 1:
                d[(i, j)] = (0, [])
            else:
                d[(i, j)] = (math.inf, [])
                for k in range(i + 1, j):
                    before = _find(i, k)
                    after = _find(k, j)
                    cost = before[0] + after[0] + n[i] * n[k] * n[j]
                    if cost < d[i, j][0]:
                        d[(i, j)] = (cost, before[1] + after[1] + [k])
        return d[(i, j)]

    return _find(0, len(n) - 1)[1]


def find_iterative(*n: int):
    """
    Возвращает последовательность оптимального перемножения матриц. Действует
    итеративным способом (снизу вверх). Последовательность [1, 3, 2] означает,
    что матрицы должны быть перемножены следующим образом ((AxB)x(CxD)).

    :param n: последовательность размеров матриц
    :return: последовательность перемножения матриц
    """
    if len(n) <= 2:
        return []
    # Используем только половину матрицы, где j >= i. Наименьшие задачи
    # расположены ближе к основной диагонали, поэтому итерируемся по диагоналям
    # Храним (cost, [multiplication order])
    d = [[(math.inf, []) for _ in n] for _ in n]
    for i in range(len(n)):
        d[i][i] = (0, [])
    for s in range(1, len(n)):
        for i in range(len(n) - s):
            j = i + s
            if i >= j - 1:
                d[i][j] = (0, [])
            for k in range(i + 1, j):
                before = d[i][k]
                after = d[k][j]
                cost = before[0] + after[0] + n[i] * n[k] * n[j]
                d[i][j] = min(d[i][j], (cost, before[1] + after[1] + [k]))
    return d[0][len(n) - 1][1]


if __name__ == '__main__':

    for func in [count_recursive, count_iterative]:
        assert func() == 0
        assert func(1) == 0
        assert func(1, 2) == 0
        assert func(1, 2, 3) == 6
        assert func(1, 2, 2, 3) == 10
        assert func(50, 20, 1, 10, 100) == 7000

    for func in [find_recursive, find_iterative]:
        assert func() == []
        assert func(1) == []
        assert func(1, 2) == []
        assert func(1, 2, 3) == [1]
        assert func(1, 2, 2, 3) == [1, 2]
        assert func(3, 2, 2, 2) == [2, 1]
        assert func(50, 20, 1, 10, 100) == [1, 3, 2]
