"""
Задача о скобках. На вход подается комбинация открывающих и закрывающих скобок
трех разных видов. Метод должен возвращать позицию некорректной скобки (начиная
с 1) или же строку 'Success', если все скобки попарно закрыты правильным
образом.
"""

from structures.stack import Stack


def resolve(s: str):
    stack = Stack()
    first_open_pos = 0
    open_brackets, close_brackets = ['(', '[', '{'], [')', ']', '}']
    for i, ch in enumerate(s, 1):
        if ch in open_brackets:
            if stack.empty():
                first_open_pos = i
            stack.push(ch)
        else:
            if stack.empty():
                return i
            else:
                opened = stack.pop()
                if open_brackets.index(opened) != close_brackets.index(ch):
                    return i
    if stack.empty():
        return 'Success'
    else:
        return first_open_pos


if __name__ == '__main__':
    assert resolve('') == 'Success'
    assert resolve('(') == 1
    assert resolve(')') == 1
    assert resolve('([]') == 1
    assert resolve('()]') == 3
    assert resolve('()[') == 3
    assert resolve('([)]') == 3
    assert resolve('()[]}') == 5
    assert resolve('{{[()]]') == 7
    assert resolve('([](){([])})') == 'Success'
