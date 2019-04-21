"""
Простые алгоритмы сортировок, основанные на пузырьковой сортировке. Все имеют
сложность О(n^2).
"""

from typing import List


def bubble_sort(lst: List):
    """
    Пузырьковая сортировка.
    """
    for i in range(len(lst) - 1):
        changed = False
        for j in range(len(lst) - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                changed = True
        if not changed:
            return lst
    return lst


def shaker_sort(lst: List):
    """
    Шейкерная сортировка.
    """
    left = 0
    right = len(lst) - 1
    while left < right:
        for i in range(left, right):
            if lst[i] > lst[i + 1]:
                lst[i], lst[i + 1] = lst[i + 1], lst[i]
        right -= 1
        for i in range(right, left, -1):
            if lst[i] < lst[i - 1]:
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
        left += 1
    return lst


def even_odd_sort(lst: List):
    """
    Четно-нечетная сортировка.
    """
    changed = True
    while changed:
        changed = False
        for i in range(1, len(lst), 2):
            if lst[i] < lst[i - 1]:
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
                changed = True
        for i in range(2, len(lst), 2):
            if lst[i] < lst[i - 1]:
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
                changed = True
    return lst


def comb_sort(lst: List):
    """
    Сортировка расческой. Первоначально осуществляет сортировку, сравнивая два
    элемента, разделенных промежутком. Промежуток определяется как предыдущий
    промежуток (или длина массива в первом случае), поделенный на 1.247. Когда
    промежуток становится равным 1, массив досортировывается пузырьком.
    Сложность алгоритма в худшем случае O(n^2), в лучшем случае О(n*log n). На
    практике асимптотика получается порядка О(n*log n), что позволяет этому
    алгоритму конкурировать с такими алгоритмами, как быстрая сортировка. Это
    неустойчивая сортировка.
    """
    factor = 1.247
    step = int(len(lst) / factor)
    while step > 1:
        for i in range(1, len(lst), step):
            if lst[i] < lst[i - 1]:
                lst[i], lst[i - 1] = lst[i - 1], lst[i]
        step = int(step / factor)
    return bubble_sort(lst)


if __name__ == '__main__':

    for func in [bubble_sort, shaker_sort, even_odd_sort, comb_sort]:
        assert func([]) == []
        assert func([1]) == [1]
        assert func([1, 2]) == [1, 2]
        assert func([2, 1]) == [1, 2]
        assert func([2, 1, 3]) == [1, 2, 3]
        assert func([2, 1, 4, 3, 3, 5]) == [1, 2, 3, 3, 4, 5]
        assert func([5, 3, 2, 3, 1, 4]) == [1, 2, 3, 3, 4, 5]
        assert func([3, 3, 2, 1, 4, 5]) == [1, 2, 3, 3, 4, 5]
        assert func([3, 3, 2, 1, 6, 4, 5]) == [1, 2, 3, 3, 4, 5, 6]
