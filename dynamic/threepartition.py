"""
3-разбиение. Нужно разбить данные n натуральных чисел на три части с равной
суммой.
"""

from typing import List


def find_partition(lst: List):
    """
    Находит оптимальное разбиение.
    """
    all_sum = sum(lst)
    if all_sum % 3 != 0:
        return False
    bucket_sum = all_sum / 3

    # a, b, c - сколько места осталось в соответствующей корзине
    # res_a, res_b, res_c - список чисел в корзине
    def _find(i, a, b, c, res_a, res_b, res_c):
        if i >= len(lst) or a < 0 or b < 0 or c < 0:
            return False
        if max(a, b, c) == lst[i] and a + b + c == lst[i]:
            if a == lst[i]:
                res_a += [lst[i]]
            elif b == lst[i]:
                res_b += [lst[i]]
            else:
                res_c += [lst[i]]
            return res_a, res_b, res_c
        return _find(i + 1, a - lst[i], b, c, res_a + [lst[i]], res_b, res_c) \
            or _find(i + 1, a, b - lst[i], c, res_a, res_b + [lst[i]], res_c) \
            or _find(i + 1, a, b, c - lst[i], res_a, res_b, res_c + [lst[i]])

    return _find(0, bucket_sum, bucket_sum, bucket_sum, [], [], [])


if __name__ == '__main__':
    assert find_partition([]) is False
    assert find_partition([3]) is False
    assert find_partition([3, 3]) is False
    assert find_partition([3, 3, 3]) == ([3], [3], [3])
    assert find_partition([1, 2, 3, 4, 4, 5, 8]) == ([1, 8], [2, 3, 4], [4, 5])
    assert find_partition([2, 2, 3, 5]) is False
