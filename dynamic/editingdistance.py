"""
Задача поиска расстояния редактирования.
"""

from typing import Sequence


def count_recursive(a: Sequence, b: Sequence):
    """
    Считает расстояние редактирования. Сложность O(len(a)*len(b)). Использует
    рекурсию и метод динамического программирования сверху вниз.
    """
    if not a and not b:
        return 0

    d = [[-1] * (len(b) + 1) for _ in range(len(a) + 1)]

    def _count(i, j):
        if i == 0:
            d[i][j] = j
        elif j == 0:
            d[i][j] = i
        elif d[i][j] == -1:
            _ins = _count(i, j - 1) + 1
            _del = _count(i - 1, j) + 1
            _change = _count(i - 1, j - 1) + (a[i - 1] != b[j - 1])
            d[i][j] = min(_ins, _del, _change)
        return d[i][j]

    return _count(len(a), len(b))


def count_iterative(a: Sequence, b: Sequence):
    """
    Считает расстояние редактирования. Сложность O(len(a)*len(b)). Использует
    метод динамического программирования снизу вверх (итерационный способ).
    """
    if not a and not b:
        return 0
    d = [[-1] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    return d[len(a)][len(b)]


def count_optimized(a: Sequence, b: Sequence):
    """
    Считает расстояние редактирования. Сложность O(len(a)*len(b)). Использует
    метод динамического программирования снизу вверх (итерационный способ).
    Вместо хранения всей матрицы хранит в памяти только два последних
    ряда/колонки (потребление памяти О(min(a, b)).
    """
    if not a and not b:
        return 0

    if len(a) < len(b):
        a, b = b, a

    prev = list(range(len(b) + 1))

    for i, ch1 in enumerate(a, 1):
        curr = [i] + [-1] * len(b)
        for j, ch2 in enumerate(b, 1):
            curr[j] = min(prev[j] + 1,
                          curr[j - 1] + 1,
                          prev[j - 1] + (ch1 != ch2))
        prev = curr
    return prev[len(b)]


def print_diff(a: Sequence, b: Sequence):
    """
    Печатает оптимальную разницу между двумя последовательностями.
    Сложность O(len(a)*len(b)) для нахождения расстояния редактирования и
    O(len(a) + len(b)) для восстановления оптимального выравнивания. Использует
    метод динамического программирования снизу вверх (итерационный способ).
    """
    if not a and not b:
        return ''

    d = [[-1] * (len(b) + 1) for _ in range(len(a) + 1)]

    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1,
                          d[i - 1][j - 1] + (a[i - 1] != b[j - 1]))
    distance = d[len(a)][len(b)]

    _a, _b, diff, i, j = '', '', '', len(a), len(b)
    while i > 0 or j > 0:
        if d[i][j] == d[i - 1][j - 1] + (a[i - 1] != b[j - 1]):
            _a += a[i - 1]
            _b += b[j - 1]
            diff += ' ' if a[i - 1] == b[j - 1] else '^'
            i -= 1
            j -= 1
        elif d[i][j] == d[i - 1][j] + 1:
            _a += a[i - 1]
            _b += '-'
            diff += '^'
            i -= 1
        else:
            _a += '-'
            _b += b[j - 1]
            diff += '^'
            j -= 1
    print(distance, "changes")
    print(_a[::-1], _b[::-1], diff[::-1], sep='\n')
    return distance


if __name__ == '__main__':
    for func in [count_recursive, count_iterative, count_optimized]:
        assert func('', '') == 0
        assert func('a', 'b') == 1
        assert func('aa', 'aa') == 0
        assert func('', 'yes') == 3
        assert func('es', 'yes') == 1
        assert func('e', 'yes') == 2
        assert func('editing', 'distance') == 5
        assert func('editing', 'diti') == 3
