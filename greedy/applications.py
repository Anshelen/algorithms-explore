"""
Задача о заявках. Дан список отрезков. Необходимо найти комбинацию из
максимального количества непересекающихся отрезков.
"""

from typing import List, Tuple


def intersects(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    """
    Проверяет пересекаются ли два отрезка.

    :param a: первый отрезок в виде кортежа (a, b), где a <= b
    :param b: второй отрезок в виде кортежа (a, b), где a <= b
    :return: True, если отрезки пересекаются
    """
    return not (a[0] >= b[1] or a[1] <= b[0])


def find_naive(sections: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Ищет комбинацию из максимального количества непересекающихся отрезков через
    поиск отрезка с минимальной правой точкой в каждой итерации.
    Сложность алгоритма O(n^2).
    """
    result = []
    while sections:
        first = min(sections, key=lambda x: x[1])
        result.append(first)
        for s in sections[:]:
            if intersects(first, s):
                sections.remove(s)
    return result


def find_sort(sections: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Ищет комбинацию из максимального количества непересекающихся отрезков через
    сортировку отрезков по их правой точке. Сложность зависит от алгоритма
    сортировки. В лучшем случае O(n*log n).
    """
    result, i = [], 0
    sections = sorted(sections, key=lambda x: x[1])
    while i < len(sections):
        chosen = sections[i]
        result.append(chosen)
        i += 1
        while i < len(sections):
            if intersects(sections[i], chosen):
                i += 1
            else:
                break
    return result


if __name__ == '__main__':

    # Проверка функции пересечения
    assert not intersects((1, 2), (2, 3))
    assert not intersects((1, 2), (3, 5))
    assert not intersects((3, 5), (1, 2))
    assert intersects((3, 10), (4, 5))
    assert intersects((1, 3), (2, 5))
    assert intersects((2, 5), (1, 3))

    # Проверка нахождения решения задачи
    for func in [find_naive, find_sort]:
        assert func([]) == []
        assert func([(1, 2)]) == [(1, 2)]
        assert func([(1, 2), (3, 5)]) == [(1, 2), (3, 5)]
        assert func([(1, 2), (3, 5), (3, 5)]) == [(1, 2), (3, 5)]
        assert func([(1, 2), (3, 5), (3.5, 4)]) == [(1, 2), (3.5, 4)]
        assert func([(1, 2), (1, 3), (3, 5), (3.5, 4)]) == [(1, 2), (3.5, 4)]
