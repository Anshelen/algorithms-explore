"""
Задача о непрерывном рюкзаке. У вора есть рюкзак некоторой грузоподъемности.
Есть ряд предметов на вынос с их весом и стоимостью. Любой предмет можно
произвольно делить, при этом его стоимость пропорционально уменьшается.
Надо определить максимальную выгоду вора.
"""

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


if __name__ == '__main__':
    assert count_price(1, []) == 0, "No goods"
    assert count_price(0, []) == 0, "Torn backpack and no goods"
    assert count_price(0, [(1, 2)]) == 0, "Torn backpack"
    assert count_price(2, [(1, 1)]) == 1, "Not enough goods"
    assert count_price(3, [(1, 1), (4, 2)]) == 5, "All goods in backpack"
    assert count_price(1, [(1, 1), (2, 2)]) == 1, "Equal capacity goods"
    assert count_price(1, [(1, 1), (4, 2)]) == 2, "Not enough capacity"
