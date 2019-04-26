"""
Быстрая сортировка. Сложность в худшем случае О(n^2), обычно O(n*log n).
Осуществляет неустойчивую сортировку на месте.
"""

import random


def _random_sep_index(lst, l, r):
    """
    Возвращает индекс i случайного разделителя в списке, такой что l<=i<=r.
    """
    return random.randint(l, r)


def _partition(lst, l, r, index_func=_random_sep_index):
    """
    Возвращает индекс элемента-разделителя i (l<=i<=r), такой что все элементы
    левее меньше или равны разделителю, а правее строго больше него. В процессе
    список изменяется.

    :param lst: список
    :param l: значение, ограничивающее индекс слева
    :param r: значение, ограничивающее индекс справа
    :param index_func: функция первоначального поиска разделителя. Дефолтно
        выбирается случайный элемент
    :return: позицию элемента-разделителя в списке
    """
    pos = index_func(lst, l, r)
    lst[l], lst[pos] = lst[pos], lst[l]
    k = l + 1
    for i in range(l + 1, r + 1):
        if lst[i] <= lst[l]:
            lst[k], lst[i] = lst[i], lst[k]
            k += 1
    lst[k - 1], lst[l] = lst[l], lst[k - 1]
    return k - 1


def _3_way_partition(lst, l, r, index_func=_random_sep_index):
    """Делит часть списка на 3 части для алгоритма быстрой сортировки

    Возвращает два индекса i, j (l<=i<=j<=r), такие что все элементы с индексами
    менее i меньше разделителя, а от j и правее - больше разделителя.
    Элементы от i до j - 1 равны разделителю. В процессе список изменяется.
    Возвращает кортеж (i, j), такой что l <= i <= j <= r и для любого k < i
    A[k] < A[i], для любого k >= j A[k] > A[i], для любого i <= k < j
    A[k] = A[i].

    Parameters
    ----------
    lst
        Список
    l
        Значение, ограничивающее индекс слева
    r
        Значение, ограничивающее индекс справа
    index_func
        Функция первоначального поиска разделителя. Дефолтно выбирается
        случайный элемент
    """
    pos = index_func(lst, l, r)
    lst[l], lst[pos] = lst[pos], lst[l]
    k1, k2 = None, l + 1
    for i in range(l + 1, r + 1):
        if lst[i] < lst[l]:
            if k1:
                lst[k1], lst[i] = lst[i], lst[k1]
                k1 += 1
            lst[k2], lst[i] = lst[i], lst[k2]
            k2 += 1
        elif lst[i] == lst[l]:
            if not k1:
                k1 = k2
            lst[k2], lst[i] = lst[i], lst[k2]
            k2 += 1
    if k1:
        k1 -= 1
    else:
        k1 = k2 - 1
    lst[k1], lst[l] = lst[l], lst[k1]
    return k1, k2


def quick_sort_random(lst, l=0, r=None):
    """
    Рекурсивный алгоритм быстрой сортировки с случайным выбором разделителя.
    """
    r = len(lst) - 1 if r is None else r
    if len(lst) <= 1 or l >= r:
        return
    m = _partition(lst, l, r)
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
        m = _partition(lst, l, r)
        quick_sort_random(lst, l, m - 1)
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
        m = _partition(lst, l, r)
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
    k1, k2 = _3_way_partition(lst, l, r)
    quick_sort_3_way_partition(lst, l, k1 - 1)
    quick_sort_3_way_partition(lst, k2, r)
