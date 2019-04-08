"""
Задача об покрытии отрезков точками. По данным отрезкам необходимо найти
множество точек минимального размера, для которого каждый из отрезков содержит
хотя бы одну из точек.
"""

from typing import List, Tuple


def find(sections: List[Tuple[int, int]]) -> List[int]:
    """
    Ищет оптимальный список точек через сортировку. Сложность алгоритма зависит
    от сложности сортировки. Обычно O(n*log n).
    """
    if not sections:
        return []
    sections = sorted(sections, key=lambda x: x[1])
    points = [sections.pop(0)[1]]
    for l, r in sections:
        if l > points[-1]:
            points.append(r)
    return points


if __name__ == '__main__':

    assert find([]) == []
    assert find([(1, 3)]) == [3]
    assert find([(1, 3), (1, 5), (1, 4)]) == [3]
    assert find([(1, 3), (2, 3), (3, 3)]) == [3]
    assert find([(1, 3), (2, 5), (3, 6)]) == [3]
    assert find([(4, 7), (1, 3), (1, 3)]) == [3, 7]
    assert find([(4, 7), (1, 3), (2, 5), (5, 6)]) == [3, 6]
    assert find([(3, 5), (1, 5), (4, 5), (0, 10)]) == [5]
