def find_naive(x: int, y: int) -> int:
    """
    Находит НОД двух положительных чисел перебором.
    """
    for i in reversed(range(max(x, y) + 1)):
        if i == 0 or x % i == y % i == 0:
            return i


def find_with_cycle(x: int, y: int) -> int:
    """
    Находит НОД двух положительных чисел. Использует алгоритм Эвклида.
    """
    while x and y:
        if x >= y:
            x %= y
        else:
            y %= x
    return max(x, y)


def find_with_recursion(x: int, y: int) -> int:
    """
    Находит НОД двух положительных чисел. Использует алгоритм Эвклида с
    рекурсией.
    """
    if x == 0 or y == 0:
        return max(x, y)
    if x >= y:
        return find_with_recursion(x % y, y)
    else:
        return find_with_recursion(x, y % x)


def find_with_recursion_without_final_if(x: int, y: int) -> int:
    """
    Находит НОД двух положительных чисел. Использует алгоритм Эвклида с
    рекурсией. Не имеет финальной проверки перед рекурсией.
    """
    if x == 0 or y == 0:
        return max(x, y)
    return find_with_recursion(y % x, x)


if __name__ == '__main__':

    functions = [find_naive, find_with_cycle, find_with_recursion,
                 find_with_recursion_without_final_if]
    for func in functions:
        assert func(0, 0) == 0
        assert func(0, 4) == 4
        assert func(11, 11) == 11
        assert func(18, 35) == 1
        assert func(14159572, 63967072) == 4
