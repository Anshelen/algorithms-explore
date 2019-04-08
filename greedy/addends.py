"""
Задача по поиску натуральных слагаемых. По данному числу n надо найти
максимальное число k, для которого n можно представить как сумму k
различных натуральных слагаемых.
"""

from typing import List


def find_addends(n: int) -> List[int]:
    """
    Находит список максимально длинный неповторяющихся натуральных слагаемых
    числа. Сложность алгоритма O(sqrt(n)).
    """
    res, addend = [], 0
    while n > 0:
        addend += 1
        if addend > n:
            # Прибавляем остаток к последнему числу
            res[-1] += n
            break
        else:
            n -= addend
            res.append(addend)
    return res


if __name__ == '__main__':
    assert find_addends(0) == []
    assert find_addends(1) == [1]
    assert find_addends(2) == [2]
    assert find_addends(3) == [1, 2]
    assert find_addends(4) == [1, 3]
    assert find_addends(6) == [1, 2, 3]
    assert find_addends(8) == [1, 2, 5]
