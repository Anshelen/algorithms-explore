"""
Задача о непрерывном рюкзаке. У вора есть рюкзак некоторой грузоподъемности.
Есть ряд предметов на вынос с их весом и стоимостью. Любой предмет можно
произвольно делить, при этом его стоимость пропорционально уменьшается.
Надо определить максимальную выгоду вора.
"""

import heapq
from typing import List, Tuple

# Отрезок [a, b] представлен кортежем (a, b)
Section = Tuple[int, int]


def count_price(capacity: int, goods: List[Section]) -> float:
    """
    Считает максимальную стоимость товаров, которые вмещаются в рюкзак.
    Сложность алгоритма зависит от сложности сортировки. Обычно O(n*log n).

    :param capacity: емкость рюкзака
    :param goods: список данных о товарах. Каждый товар представлен в виде
        кортежа (a, b), где a - суммарная стоимость товара, b - вес товара
    :return: максимальная стоимость товаров
    """
    price = 0
    goods = sorted(goods, key=lambda x: x[0] / x[1], reverse=True)
    while goods and capacity:
        good = goods.pop(0)
        cost, amount = good[0], good[1]
        can_take = min(capacity, amount)
        price += can_take / amount * cost
        capacity -= can_take
    return price


def count_price_with_heap(capacity: int, goods: List[Section]) -> float:
    """
    Считает максимальную стоимость товаров, которые вмещаются в рюкзак.
    Использует мин-кучу heapq из стандартной библиотеки. Сложность в худшем
    случае O(n*log n). Если емкость рюкзака много меньше количества товаров,
    то сложность алгоритма будет близка к линейной. Более быстрый вариант, чем
    при использовании сортировки.

    :param capacity: емкость рюкзака
    :param goods: список данных о товарах. Каждый товар представлен в виде
        кортежа (a, b), где a - суммарная стоимость товара, b - вес товара
    :return: максимальная стоимость товаров
    """
    heap_data = [(-price / amount, amount) for price, amount in goods]
    heapq.heapify(heap_data)
    price = 0
    while heap_data and capacity:
        value, amount = heapq.heappop(heap_data)
        can_take = min(capacity, amount)
        price += can_take * -value
        capacity -= can_take
    return price


if __name__ == '__main__':

    for func in [count_price, count_price_with_heap]:
        assert func(1, []) == 0, "No goods"
        assert func(0, []) == 0, "Torn backpack and no goods"
        assert func(0, [(1, 2)]) == 0, "Torn backpack"
        assert func(2, [(1, 1)]) == 1, "Not enough goods"
        assert func(3, [(1, 1), (4, 2)]) == 5, "All goods in backpack"
        assert func(1, [(1, 1), (2, 2)]) == 1, "Equal capacity goods"
        assert func(1, [(1, 1), (4, 2)]) == 2, "Not enough capacity"
