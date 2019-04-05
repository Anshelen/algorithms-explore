class FibGenerator:
    """
    Генератор, вычисляющий числа Фибоначчи.
    """
    def __init__(self):
        self.a, self.b = 0, 1

    def __iter__(self):
        return self

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b
        return self.a


def find_with_recursion(n: int) -> int:
    """
    Вычисление числа Фибоначчи через рекурсию.
    """
    if n in [1, 2]:
        return 1
    return find_with_recursion(n - 1) + find_with_recursion(n - 2)


def find_with_list(n: int) -> int:
    """
    Вычисление числа Фибоначчи с использованием списка.
    """
    lst = [0, 1]
    if n == 1:
        return lst[n]
    for i in range(2, n + 1):
        lst.append(lst[i-1] + lst[i-2])
    return lst[n]


def find_with_two_variables(n: int) -> int:
    """
    Вычисление числа Фибоначчи с использованием двух переменных.
    """
    a, b = 0, 1
    if n == 1:
        return b
    for i in range(2, n + 1):
        a, b = b, a + b
    return b


def find_last_digit(n: int) -> int:
    """
    Дано число 1≤n≤107, необходимо найти последнюю цифру n-го числа Фибоначчи.
    """
    a, b = 0, 1
    if n == 1:
        return b
    for _ in range(2, n + 1):
        a, b = b, (a + b) % 10
    return b


def find_pezano_period_list(m):
    """
    Возвращает список остатков от деления последовательности Фибоначи на m
    (1≤m≤10^5) с длиной, равной периоду Пизано.

    :param m: делитель
    :return: период Пизано
    """
    a, b, pezano_lst = 0, 1, [0, 1]
    if m == 1:
        return [0]
    # Максимально период равен 6 * m для всех положительных целых m
    for _ in range(6 * m):
        a, b = b, (a + b) % m
        pezano_lst.append(b)
        # Проверяем не начался ли новый период. Период всегда начинается с 0 и 1
        if pezano_lst[-2] == 0 and pezano_lst[-1] == 1:
            break
    return pezano_lst[:-2]


def find_mod(n: int, m: int) -> int:
    """
    Ищет остаток от деления n-ного числа Фибоначчи на число m (1≤n≤10^18
    и 2≤m≤10^5)

    :param n: номер числа Фибоначчи
    :param m: делитель
    :return: остаток от деления n-ного числа Фибоначчи на m
    """
    lst = find_pezano_period_list(m)
    return lst[n % len(lst)]


if __name__ == "__main__":

    # Дано целое число 1≤n≤40, необходимо вычислить n-е число Фибоначчи
    # (напомним, что F0=0, F1=1 и Fn=Fn−1+Fn−2 при n≥2)
    functions = [find_with_two_variables, find_with_list, find_with_recursion]
    for func in functions:
        assert func(1) == 1
        assert func(2) == 1
        assert func(3) == 2
        assert func(20) == 6765

    # Дано число 1≤n≤107, необходимо найти последнюю цифру n-го числа Фибоначчи
    assert find_last_digit(1) == 1
    assert find_last_digit(2) == 1
    assert find_last_digit(5) == 5
    assert find_last_digit(317457) == 2

    # Тестирование генератора чисел Фибоначчи
    gen = FibGenerator()
    fib_numbers = [1, 1, 2, 3, 5]
    for i in range(5):
        assert next(gen) == fib_numbers[i]

    # Тестирование периода Пизано
    assert find_pezano_period_list(4) == [0, 1, 1, 2, 3, 1]
    pezano_periods = [1, 3, 8, 6, 20, 24, 16, 12, 24, 60, 10, 24, 28, 48, 40, 24]
    for i in range(1, len(pezano_periods)):
        assert len(find_pezano_period_list(i)) == pezano_periods[i - 1]

    # Даны целые числа 1≤n≤10^18 и 2≤m≤10^5, необходимо найти остаток от деления
    # n-го числа Фибоначчи на m
    fib_num = 10
    fib = find_with_two_variables(fib_num)
    for i in range(1, 20):
        assert find_mod(fib_num, i) == fib % i
