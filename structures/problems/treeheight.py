"""
Поиск высоты дерева. Строка содержит n целых неотрицательных чисел
parent(0),... ,parent(n−1). Для каждого 0 ≤ i ≤ n − 1, parent(i) — родитель
вершины i; если parent(i) = −1, то i является корнем. Гарантируется, что корень
ровно один. Гарантируется, что данная последовательность задаёт дерево.
Например, последовательность 4 -1 4 1 1 задает следующее дерево с высотой 3:
    1
  /   \
3       4
      /   \
    0       2
"""

from typing import List

from structures.stack import Stack
from structures.tree import build_tree


def find_recursive(lst: List[int]) -> int:
    """
    Ищет высоту дерева. Рекурсивный алгоритм без построения дерева.
    Имеет сложность О(n^2).
    """

    def _find(root_value):
        res = []
        for i in range(len(lst)):
            if lst[i] == root_value:
                res.append(_find(i))
        if not res:
            return 1
        return max(res) + 1

    return _find(lst.index(-1))


def find_iterative(lst: List[int]) -> int:
    """
    Ищет высоту дерева. Итеративный алгоритм без построения дерева.
    Имеет сложность О(n^2).
    """
    root_value, root_depth = lst.index(-1), 1
    max_depth = 1
    tasks = Stack()
    tasks.push((root_value, root_depth))
    while tasks:
        v = tasks.pop()
        value, depth = v[0], v[1]
        if max_depth < depth:
            max_depth = depth
        for i in range(len(lst)):
            if lst[i] == value:
                tasks.push((i, depth + 1))
    return max_depth


def find_iterative_building_tree(lst: List[int]) -> int:
    """
    Ищет высоту дерева. Итеративный алгоритм с постоением дерева. Сложность
    алгоритма О(n).
    """
    root = build_tree(lst)
    root.level = 1

    max_level = 1
    tasks = Stack()
    tasks.push(root)
    while tasks:
        node = tasks.pop()
        if max_level < node.level:
            max_level = node.level
        for child in node.children:
            child.level = node.level + 1
            tasks.push(child)
    return max_level


if __name__ == '__main__':
    for func in [find_recursive, find_iterative, find_iterative_building_tree]:
        assert func([-1]) == 1
        assert func([-1, 0, 1]) == 3
        assert func([4, -1, 4, 1, 1]) == 3
        assert func([-1, 0, 4, 0, 3]) == 4
        assert func([9, 7, 5, 5, 2, 9, 9, 9, 2, -1]) == 4
