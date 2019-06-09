"""
Алгоритм Рабина — Карпа.

Алгоритм поиска, который ищет шаблон, то есть подстроку, в тексте, используя
хеширование. Для текста длины n и шаблона длины m его среднее и лучшее время
исполнения равно O(n), в худшем случае он имеет эффективность O(n*m).
"""

from typing import List


def find_matches(text: str, pattern: str) -> List[int]:
    """
    Ищет все индексы вхождений строки pattern в строку text.
    """

    if not text or not pattern or len(pattern) > len(text):
        return []
    if len(pattern) == 1:
        res = []
        for i in range(len(text)):
            if text[i] == pattern:
                res.append(i)
        return res

    # Простое число. Это число Мерсенна хорошо работает на 64-битной архитектуре
    p = 2 << 61 - 1
    # Любое число в интервале [1, p - 1]
    x = 263
    curr_hash, template_hash = 0, 0

    x_acc = 1  # Содержит степень x**(len(template) - 1)
    for i in range(len(pattern)):
        curr_hash = (curr_hash + x_acc * ord(
            text[len(text) - len(pattern) + i])) % p
        template_hash = (template_hash + x_acc * ord(pattern[i])) % p
        if i < len(pattern) - 1:
            x_acc = (x_acc * x) % p

    res = []
    i = len(text) - len(pattern)
    while True:
        if curr_hash == template_hash and text[i:i + len(pattern)] == pattern:
            res.append(i)
        i -= 1
        if i < 0:
            break
        curr_hash \
            = ((curr_hash - (ord(text[i + len(pattern)]) * x_acc) % p) * x
               + ord(text[i])) % p
    res.reverse()
    return res


if __name__ == '__main__':
    assert find_matches('', 'a') == []
    assert find_matches('a', 'a') == [0]
    assert find_matches('a', '') == []
    assert find_matches('aaa', 'a') == [0, 1, 2]
    assert find_matches('a', 'aaa') == []
    assert find_matches('aba', 'b') == [1]
    assert find_matches('aba', 'ba') == [1]
    assert find_matches('aba', 'c') == []
    assert find_matches('aba', 'ca') == []
    assert find_matches('ababaffdaba', 'aba') == [0, 2, 8]
    assert find_matches('abacaba', 'aba') == [0, 4]
