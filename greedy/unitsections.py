"""
Задача о покрытии точек единичными отрезками. Необходимо найти минимальное
количество единичных отрезков, которыми можно "покрыть" все переданные точки.
"""

from typing import List, Tuple


def find_naive(points: List[int]) -> List[Tuple[int, int]]:
    """
    Ищет оптимальное количество отрезков через поиск минимальной точки в каждой
    итерации. Алгоритм имеет сложность O(n^2).
    """
    result = []
    while points:
        left = min(points)
        result.append((left, left + 1))
        for point in points[:]:
            if left <= point <= left + 1:
                points.remove(point)
    return result


def find_sort(points: List[int]) -> List[Tuple[int, int]]:
    """
    Ищет оптимальное количество отрезков через сортировку. Алгоритм имеет
    сложность в зависимости от сложности алгоритма сортировки. В лучшем случае
    O(n*log n).
    """
    result, i = [], 0
    points = sorted(points)
    while i < len(points):
        left = points[i]
        result.append((left, left + 1))
        while i < len(points):
            if left <= points[i] <= left + 1:
                i += 1
            else:
                break
    return result


if __name__ == '__main__':

    for func in [find_naive, find_sort]:
        assert func([]) == []
        assert func([1]) == [(1, 2)]
        assert func([1, 1, 1]) == [(1, 2)]
        assert func([1, 1.6, 2]) == [(1, 2)]
        assert func([1, 2, 3, 3.5, 7]) == [(1, 2), (3, 4), (7, 8)]
        assert func([7, 3, 2, 3.5, 1]) == [(1, 2), (3, 4), (7, 8)]
