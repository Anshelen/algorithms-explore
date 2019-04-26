"""
Алгоритм сортировки вставками. Сложность О(n^2).
"""

from typing import List


def insertion_sort(lst: List):
    """
    Сортировка вставками.
    """
    for i in range(1, len(lst)):
        j = i
        while j > 0:
            if lst[j] < lst[j - 1]:
                lst[j], lst[j - 1] = lst[j - 1], lst[j]
                j -= 1
            else:
                break
    return lst


def insertion_sort_with_buffer(lst: List):
    """
    Сортировка вставками с помощью буффера. Хотя буфер по-идее и не нужен,
    почему то классический алгоритм именно с буффером.
    """
    for i in range(1, len(lst)):
        buf, lst[i] = lst[i], None
        j = i - 1
        while j >= 0:
            if lst[j] > buf:
                lst[j + 1], lst[j] = lst[j], lst[j + 1]
                j -= 1
            else:
                lst[j + 1] = buf
                break
        else:
            lst[0] = buf
    return lst


def pair_insertion_sort(lst: List):
    """
    Парная сортировка простыми вставками. Экономит на обработке меньшего
    элемента из пары. Для него поиск точки вставки и сама вставка осуществляются
    только на той отсортированной части массива, в которую не входит
    отсортированная область, задействованная для обработки большего элемента
    из пары. Сложность алгоритма так же О(n^2), но он быстрее обычной сортировки
    вставками. Обычно используется для сортировки малых массивов или небольших
    участков крупных массивов.
    """
    for i in range(0, len(lst), 2):
        if i == len(lst) - 1:
            # Обычная сортировка вставками для последнего нечетного элемента
            buf, lst[i] = lst[i], None
            j = i - 1
            while j >= 0:
                if lst[j] > buf:
                    lst[j + 1], lst[j] = lst[j], lst[j + 1]
                    j -= 1
                else:
                    lst[j + 1] = buf
                    break
            else:
                lst[0] = buf
        else:
            small, big = min(lst[i], lst[i + 1]), max(lst[i], lst[i + 1])
            # Для дебага. Не влияет на сортировку
            lst[i], lst[i + 1] = None, None
            j = i - 1
            # Проходим для большого элемента
            while j >= 0:
                if lst[j] > big:
                    lst[j], lst[j + 2] = lst[j + 2], lst[j]
                    j -= 1
                else:
                    lst[j + 2] = big
                    break
            else:
                lst[1] = big

            # Продолжаем проход теперь для малого элемента
            while j >= 0:
                if lst[j] > small:
                    lst[j], lst[j + 1] = lst[j + 1], lst[j]
                    j -= 1
                else:
                    lst[j + 1] = small
                    break
            else:
                lst[0] = small
    return lst
