"""
Быстрая сортировка. Сложность в худшем случае О(n^2), обычно O(n*log n).
Осуществляет неустойчивую сортировку на месте.
"""

from sorts.partitions import partition, three_way_partition


def quick_sort_random(lst, l=0, r=None):
    """
    Рекурсивный алгоритм быстрой сортировки с случайным выбором разделителя.
    """
    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1 or l >= r:
        return
    m = partition(lst, l, r)
    quick_sort_random(lst, l, m - 1)
    quick_sort_random(lst, m + 1, r)


def quick_sort_no_tail_recursion(lst, l=0, r=None):
    """
    Рекурсивный алгоритм быстрой сортировки без хвостовой рекурсии. Разделитель
    определяется случайным образом.
    """
    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1:
        return
    while l < r:
        m = partition(lst, l, r)
        quick_sort_no_tail_recursion(lst, l, m - 1)
        l = m + 1


def quick_sort_no_recursion(lst, l=0, r=None):
    """
    Алгоритм быстрой сортировки без рекурсии. Разделитель определяется случайным
    образом.
    """
    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1:
        return
    q = [(l, r)]
    while q:
        l, r = q.pop(0)
        if l >= r:
            continue
        m = partition(lst, l, r)
        q.append((l, m - 1))
        q.append((m + 1, r))


def quick_sort_3_way_partition(lst, l=0, r=None):
    """
    Рекурсивный алгоритм быстрой сортировки с тройным разделением и случайным
    выбором разделителя. Тройное разделение значительно ускоряет алгоритм, если
    в списке много одинаковых элементов.
    """
    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1 or l >= r:
        return
    k1, k2 = three_way_partition(lst, l, r)
    quick_sort_3_way_partition(lst, l, k1 - 1)
    quick_sort_3_way_partition(lst, k2, r)
