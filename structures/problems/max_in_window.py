"""
Задача о максимуме в скользящем окне.

Нужно найти максимум в каждом окне размера m данного массива чисел A[1 . . . n]
за линейное время.
"""

from typing import Sequence, Union, List

from structures.max_queue import MaxQueue

Num = Union[int, float]


def find_maximums(lst: Sequence[Num], window_size: int) -> List[Num]:
    if not lst or window_size <= 0:
        return []
    if window_size > len(lst):
        window_size = len(lst)

    q = MaxQueue()
    res = []
    for i in range(window_size):
        q.push(lst[i])
    res.append(q.max())
    for i in range(window_size, len(lst)):
        q.pop()
        q.push(lst[i])
        res.append(q.max())
    return res


if __name__ == '__main__':
    assert find_maximums([], 1) == []
    assert find_maximums([1], 0) == []
    assert find_maximums([1], 2) == [1]
    assert find_maximums([2, 1, 5], 1) == [2, 1, 5]
    assert find_maximums([2, 3, 9], 3) == [9]
    assert find_maximums([2, 3, 9], 4) == [9]
    assert find_maximums([2, 7, 3, 1, 5, 2, 6, 2], 4) == [7, 7, 5, 6, 6]
