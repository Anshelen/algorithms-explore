"""
Задача о рюкзаке. Бывает в двух вариациях:
1. С повторами. В рюкзак можно поместить бесконечное количество одного товара
из набора.
2. Без повторов. Каждый товар из набора может быть помещен в рюкзак только
единожды.
Сложность алгоритмов O(len(items) * weight). Метод динамического
программирования сверху вниз (рекурсивный) в данном случае эффективней метода
снизу вверх (итеративный), так как он при подсчете считает только нужные
комбинации, а не все.
"""

from typing import List, Tuple

# Предмет представлен кортежем (weight, price)
Item = Tuple[int, int]


def count_with_repeats(items: List[Item], weight: int):
    """
    Считает стоимость рюкзака с повторениями итеративным методом (снизу вверх).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: стоимость оптимально заполненного рюкзака
    """
    # Список [0..i] со стоимостями оптимально заполненного рюкзака с весом i
    d = [0 for _ in range(weight + 1)]
    for w in range(weight + 1):
        for item_weight, item_price in items:
            if item_weight <= w:
                d[w] = max(d[w], d[w - item_weight] + item_price)
    return d[weight]


def count_with_repeats_recursive(items: List[Item], weight: int):
    """
    Считает стоимость рюкзака с повторениями рекурсивным методом (сверху вниз).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: стоимость оптимально заполненного рюкзака
    """
    # Словарь, содержащий пары weight: optimal price
    d = {}

    def _count(items, weight):
        if weight not in d:
            d[weight] = 0
            for item_width, item_price in items:
                if item_width <= weight:
                    d[weight] = max(d[weight],
                                    _count(items,
                                           weight - item_width) + item_price)
        return d[weight]

    return _count(items, weight)


def find_with_repeats(items: List[Item], weight: int):
    """
    Возвращает оптимальное заполнение рюкзака с повторениями итеративным методом
    (снизу вверх).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: список предметов, обеспечивающих оптимальное заполнение
    """
    # В d[i] хранятся максимальная стоимость рюкзака веса i и список предметов,
    # которые составляют оптимальный набор
    d = [(0, []) for _ in range(weight + 1)]
    for w in range(weight + 1):
        for item in items:
            item_width, item_price = item[0], item[1]
            if item_width <= w:
                # Оптимальный поднабор, если item включен в оптимальный набор
                _opt = d[w - item_width][0] + item_price
                if _opt > d[w][0]:
                    d[w] = (_opt, d[w - item_width][1] + [item])
    res = d[weight][1]
    res.reverse()
    return res


def find_with_repeats_recursive(items: List[Item], weight: int):
    """
    Возвращает оптимальное заполнение рюкзака с повторениями рекурсивным методом
    (сверху вниз).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: список предметов, обеспечивающих оптимальное заполнение
    """
    # Хранит weight: (price, [optimal items])
    d = {}

    def _find(items, weight):
        if weight not in d:
            d[weight] = (0, [])
            for item in items:
                item_weight, item_price = item[0], item[1]
                if item_weight <= weight:
                    # Оптимальный поднабор при условии, что item в оптимальном
                    # наборе
                    _opt = _find(items, weight - item_weight)
                    _opt_price = _opt[0] + item_price
                    if _opt_price > d[weight][0]:
                        d[weight] = (_opt_price, _opt[1] + [item])
        return d[weight]

    res = _find(items, weight)[1]
    res.reverse()
    return res


def count_without_repeats(items: List[Item], weight: int):
    """
    Считает стоимость рюкзака без повторений итеративным методом (снизу вверх).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: стоимость оптимально заполненного рюкзака
    """
    # Двумерный массив, содержащий стоимости всех возможных комбинаций
    # весов и предметов
    d = [[0 for _ in range(len(items) + 1)] for _ in range(weight + 1)]
    for i in range(1, len(items) + 1):
        for w in range(1, weight + 1):
            d[w][i] = d[w][i - 1]
            item_weight, item_price = items[i - 1][0], items[i - 1][1]
            if item_weight <= w:
                d[w][i] = max(d[w][i], d[w - item_weight][i - 1] + item_price)
    return d[weight][len(items)]


def count_without_repeats_recursive(items: List[Item], weight: int):
    """
    Считает стоимость рюкзака без повторений рекурсивным методом (сверху вниз).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: стоимость оптимально заполненного рюкзака
    """
    # Хранит пары: (index, weight): price
    d = {}

    # max_index - верхний индекс предметов, т.е. рассматриваем предметы с
    # индексами в диапазоне [0, max_index)
    def _count(max_index, weight):
        if (max_index, weight) not in d:
            if max_index == 0 or weight <= 0:
                d[(max_index, weight)] = 0
            else:
                tasks = []
                item_weight, item_price \
                    = items[max_index - 1][0], items[max_index - 1][1]
                if item_weight <= weight:
                    # Предмет присутствует в оптимальном наборе
                    tasks.append(_count(max_index - 1,
                                        weight - item_weight) + item_price)
                # Предмет отсутствует в оптимальном наборе
                tasks.append(_count(max_index - 1, weight))
                d[(max_index, weight)] = max(tasks)
        return d[(max_index, weight)]

    return _count(len(items), weight)


def find_without_repeats(items: List[Item], weight: int):
    """
    Возвращает оптимальное заполнение рюкзака без повторов итеративным методом
    (снизу вверх).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: список предметов, обеспечивающих оптимальное заполнение рюкзака
    """
    d = [[0 for _ in range(len(items) + 1)] for _ in range(weight + 1)]
    for i in range(1, len(items) + 1):
        for w in range(1, weight + 1):
            d[w][i] = d[w][i - 1]
            item_weight, item_price = items[i - 1][0], items[i - 1][1]
            if item_weight <= w:
                d[w][i] = max(d[w][i], d[w - item_weight][i - 1] + item_price)
    res = []
    # Обходим матрицу d заново, чтоб восстановить события
    for i in range(len(items), 0, -1):
        if d[weight][i] != d[weight][i - 1]:
            res.append(items[i - 1])
            weight -= items[i - 1][0]
    res.reverse()
    return res


def find_without_repeats_recursive(items: List[Item], weight: int):
    """
    Возвращает оптимальное заполнение рюкзака без повторов рекурсивным методом
    (сверху вниз).

    :param items: список предметов в виде кортежей (weight, price)
    :param weight: вместимость рюкзака
    :return: список предметов, обеспечивающих оптимальное заполнение рюкзака
    """
    # Хранит пары: (last_index, weight): (price, [optimal items])
    d = {}

    def _find(index, weight):
        if (index, weight) not in d:
            if index == 0 or weight <= 0:
                d[(index, weight)] = (0, [])
            else:
                tasks = []
                item = items[index - 1]
                item_weight, item_price = item[0], item[1]
                if item_weight <= weight:
                    # item в оптимальном наборе
                    _opt = _find(index - 1, weight - item_weight)
                    tasks.append((_opt[0] + item_price, _opt[1] + [item]))
                # item не присутствует в оптимальном наборе
                tasks.append(_find(index - 1, weight))
                d[(index, weight)] = max(tasks)
        return d[(index, weight)]

    return _find(len(items), weight)[1]


if __name__ == '__main__':

    for func in [count_with_repeats, count_with_repeats_recursive]:
        assert func([], 1) == 0
        assert func([(6, 30)], 1) == 0
        assert func([(6, 30)], 6) == 30
        assert func([(6, 30)], 7) == 30
        assert func([(6, 30)], 12) == 60
        assert func([(6, 30), (3, 14), (4, 16), (2, 9)], 10) == 48

    for func in [find_with_repeats, find_with_repeats_recursive]:
        assert func([], 1) == []
        assert func([(6, 30)], 1) == []
        assert func([(6, 30)], 6) == [(6, 30)]
        assert func([(6, 30)], 7) == [(6, 30)]
        assert func([(6, 30)], 12) == [(6, 30), (6, 30)]
        assert func([(6, 30), (3, 14), (4, 16), (2, 9)], 10) == [(6, 30),
                                                                 (2, 9), (2, 9)]

    for func in [count_without_repeats, count_without_repeats_recursive]:
        assert func([], 1) == 0
        assert func([(6, 30)], 1) == 0
        assert func([(6, 30)], 6) == 30
        assert func([(6, 30)], 7) == 30
        assert func([(6, 30)], 12) == 30
        assert func([(6, 30), (3, 14), (4, 16), (2, 9)], 10) == 46

    for func in [find_without_repeats, find_without_repeats_recursive]:
        assert func([], 1) == []
        assert func([(6, 30)], 1) == []
        assert func([(6, 30)], 6) == [(6, 30)]
        assert func([(6, 30)], 7) == [(6, 30)]
        assert func([(6, 30)], 12) == [(6, 30)]
        assert func([(6, 30), (3, 14), (4, 16), (2, 9)], 10) == [(6, 30),
                                                                 (4, 16)]
