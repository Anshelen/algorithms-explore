"""
Задача о системе равенств и неравенств.

Проверить, можно ли присвоить переменным целые значения, чтобы выполнить
заданные равенства вида Xi = Xj и неравенства вида Xp != Xq.
"""
from typing import Tuple, Iterable

from structures.disjoint_sets import MathDisjointSets

# Пара номеров сравниваемых переменных
Pair = Tuple[int, int]


def check(eq_pairs: Iterable[Pair], ne_pairs: Iterable[Pair]) -> bool:
    """
    Проверяет возможно ли присвоить переменным целые значения.

    :param eq_pairs: пары (i, j), для которых верно условию Xi = Xj
    :param ne_pairs: пары (p, q), для которых верно условию Xp != Xq
    """
    s = MathDisjointSets()
    ids = {}
    for i, j in eq_pairs:
        if i not in ids:
            ids[i] = s.make_set()
        if j not in ids:
            ids[j] = s.make_set()
        s.union(ids[i], ids[j])
    for p, q in ne_pairs:
        if p == q or (p in ids and q in ids and s.find_root_id(
                ids[p]) == s.find_root_id(ids[q])):
            return False
    return True


if __name__ == '__main__':
    assert check([], [])
    assert check([(1, 3)], [])
    assert not check([], [(1, 1)])
    assert check([(1, 3)], [(1, 2)])
    assert not check([(1, 3), (2, 3)], [(1, 2)])
    assert check([(1, 3), (2, 3)], [(1, 5)])
    assert check([(1, 3), (2, 3)], [(1, 5), (1, 6), (4, 5)])
    assert not check([(1, 3), (2, 3), (3, 5)], [(1, 5), (1, 6), (4, 5)])
