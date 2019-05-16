"""
Задача поиска наибольшей возрастающей последовательности.
"""

from typing import List


def find_lis(lst: List):
    """
    Ищет наибольшую возрастающую последовательность. Сложность О(n^2).
    """
    if not lst:
        return []
    # В length_arr храним длины НВП
    length_arr = []
    for i in range(len(lst)):
        length_arr.append(1)
        for j in range(i):
            if lst[j] < lst[i] and length_arr[i] <= length_arr[j]:
                length_arr[i] = length_arr[j] + 1
    length = max(length_arr)
    index = length_arr.index(length)
    res = [lst[index]]
    for i in range(index, -1, -1):
        if length_arr[i] == length - 1 and lst[i] < res[-1]:
            res.append(lst[i])
            length -= 1
        if length == 0:
            break
    res.reverse()
    return res


def find_lis_optimal(lst: List):
    """
    Ищет наибольшую возрастающую последовательность. Сложность О(n*log n).
    Внутри использует двоичный поиск.
    """
    import bisect
    if not lst:
        return []
    # Массив с длинами НВП различных длин и массив с соответствующими элементами
    length_arr = [0]
    length_arr_el = [lst[0]]
    # Массив, содержащий ссылки на элементы последовательности
    seq = [-1 for _ in lst]
    for i in range(1, len(lst)):
        el = lst[i]
        if el > length_arr_el[-1]:
            seq[i] = length_arr[-1]
            length_arr.append(i)
            length_arr_el.append(lst[i])
        else:
            pos = bisect.bisect_left(length_arr_el, lst[i])
            if pos > 0:
                seq[i] = length_arr[pos - 1]
            length_arr[pos] = i
            length_arr_el[pos] = lst[i]
    res = []
    last_index = length_arr[-1]
    while last_index > -1:
        res.append(lst[last_index])
        last_index = seq[last_index]
    res.reverse()
    return res


def find_lnis_optimal(lst: List):
    """
    Ищет наибольшую невозрастающую последовательность. Сложность О(n*log n).
    Внутри использует двоичный поиск.
    """
    import bisect
    if not lst:
        return []
    # Массив с длинами НВП различных длин и массив с соответствующими элементами
    length_arr = [0]
    length_arr_el = [-1 * lst[0]]
    # Массив, содержащий ссылки на элементы последовательности
    seq = [-1 for _ in lst]
    for i in range(1, len(lst)):
        el = lst[i]
        if el <= -1 * length_arr_el[-1]:
            seq[i] = length_arr[-1]
            length_arr.append(i)
            length_arr_el.append(-1 * lst[i])
        else:
            pos = bisect.bisect_right(length_arr_el, -1 * lst[i])
            if pos > 0:
                seq[i] = length_arr[pos - 1]
            length_arr[pos] = i
            length_arr_el[pos] = -1 * lst[i]
    res = []
    last_index = length_arr[-1]
    while last_index > -1:
        res.append(lst[last_index])
        last_index = seq[last_index]
    res.reverse()
    return res


if __name__ == '__main__':
    for func in [find_lis, find_lis_optimal]:
        assert func([]) == []
        assert func([2]) == [2]
        assert func([2, 2]) == [2]
        assert func([2, 3]) == [2, 3]
        assert func([5, 2, 3]) == [2, 3]
        assert func([3, 4, 5, 2, 3, 3, 6]) == [3, 4, 5, 6]

    assert find_lnis_optimal([]) == []
    assert find_lnis_optimal([2]) == [2]
    assert find_lnis_optimal([2, 2]) == [2, 2]
    assert find_lnis_optimal([2, 3]) == [3]
    assert find_lnis_optimal([5, 2, 3]) == [5, 3]
    assert find_lnis_optimal([8, 5, 7, 3, 1, 4, 0, 0, 4, 2, 1]) == [8, 7, 4, 4,
                                                                    2, 1]
