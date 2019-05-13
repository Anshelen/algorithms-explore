"""
Интроспективная сортировка. К омбинированный рекурсивный алгоритм быстрой
сортировки с выбором разделителя по медиане и сортировки слиянием. Если
глубина рекурсии превышает c*log n, то запускается сортировка слиянием. Таким
образом сложность алгоритма в худшем случае O(n*log n).
"""

import math

from sorts.mergesort import merge_sort_iterative
from sorts.partitions import partition, three_way_partition, median_sep_index


def introsort(lst, l=0, r=None):
    """
    Интроспективная сортировка.
    """
    max_depth = 3 * math.log2(len(lst) + 1)

    def _quick_sort(lst, l=0, r=None, depth=0):
        depth += 1
        if depth > max_depth:
            return False

        r = len(lst) - 1 if r is None else r
        if len(lst) <= 1:
            return True

        if l >= r:
            return True

        m = partition(lst, l, r, index_func=median_sep_index)
        res1 = _quick_sort(lst, l, m - 1, depth)
        res2 = _quick_sort(lst, m + 1, r, depth)
        if depth > max_depth:
            return False

        depth -= 1
        return res1 and res2

    success = _quick_sort(lst, l, r)
    if not success:
        sorted_lst = merge_sort_iterative(lst)
        lst.clear()
        lst.extend(sorted_lst)


def optimized_introsort(lst, l=0, r=None):
    """Улучшенная интроспективная сортировка

    Алгоритм интроспективной сортировки, включающий в себя ряд оптимизаций,
    а именно:
        1. Весь алгоритм итеративный (без рекурсии)
        2. Алгоритм быстрой сортировки использует тройное разделение
    """
    max_depth = 3 * math.log2(len(lst) + 1)
    out_of_depth = False

    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1:
        return
    q = [(l, r, 1)]
    while q:
        l, r, depth = q.pop(0)
        if depth > max_depth:
            out_of_depth = True
            break
        if l >= r:
            continue
        k1, k2 = three_way_partition(lst, l, r, index_func=median_sep_index)
        q.append((l, k1 - 1, depth + 1))
        q.append((k2, r, depth + 1))

    if out_of_depth:
        sorted_lst = merge_sort_iterative(lst)
        lst.clear()
        lst.extend(sorted_lst)
