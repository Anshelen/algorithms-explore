"""
Есть примитивный калькулятор, который умеет выполнять всего три операции с
текущим числом x: заменить x на 2x, 3x или x+1. По данному целому числу
определите последовательность промежуточных чисел, получаемых в результате
минимального числа операций k, необходимого, чтобы получить n из 1.
"""


def find_iterative(n: int):
    """
    Ищет последовательность промежуточных чисел для калькулятора итеративным
    способом (снизу вверх). Сложность алгоритма линейная.
    """
    # Для удобства начнем список с 1, а не 0. В списке кортеж
    # (operations count, previous number)
    d = [(None, None), (0, 1)]
    for i in range(2, n + 1):
        tasks = [(d[i - 1][0] + 1, i - 1)]
        if i >= 3 and i % 3 == 0:
            tasks.append((d[i // 3][0] + 1, i // 3))
        if i >= 2 and i % 2 == 0:
            tasks.append((d[i // 2][0] + 1, i // 2))
        d.append(min(tasks))

    res, i = [], n
    while i != 1:
        res.append(i)
        i = d[i][1]
    res.append(1)
    res.reverse()
    return res


if __name__ == '__main__':
    assert find_iterative(1) == [1]
    assert find_iterative(2) == [1, 2]
    assert find_iterative(5) == [1, 2, 4, 5]
    assert find_iterative(16) == [1, 2, 4, 8, 16]
    assert find_iterative(96234) == [1, 3, 9, 10, 11, 22, 66, 198, 594, 1782,
                                     5346, 16038, 16039, 32078, 96234]
