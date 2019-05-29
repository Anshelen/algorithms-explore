"""
Формирование дерева. Строка содержит n целых неотрицательных чисел
parent(0),... ,parent(n−1). Для каждого 0 ≤ i ≤ n − 1, parent(i) — родитель
вершины i; если parent(i) = −1, то i является корнем. Гарантируется, что корень
ровно один. Гарантируется, что данная последовательность задаёт дерево.
Например, последовательность 4 -1 4 1 1 задает следующее дерево:
    1
  /   \
3       4
      /   \
    0       2
"""
import unittest
from typing import List


class TreeNode:
    """
    Узел дерева.
    """

    def __init__(self, value: int = None, parent: 'TreeNode' = None,
                 children: List['TreeNode'] = None) -> None:
        self.value = value
        self.parent = parent
        self.children = children if children is not None else []


def build_tree(lst: List[int]) -> TreeNode:
    """
    Строит дерево по списку. Возвращает корень дерева. Сложность О(n).
    """
    res = [TreeNode() for _ in lst]
    root = -1
    for i in range(len(lst)):
        res[i].value = i
        if lst[i] == -1:
            root = i
        else:
            res[i].parent = res[lst[i]]
            res[lst[i]].children.append(res[i])
    return res[root]


class BuildTreeTests(unittest.TestCase):

    def assertTreeEqual(self, root, expected):
        def _check(a, b):
            self.assertEqual(a.value, b.value)
            self.assertEqual(len(a.children), len(b.children))
            for i in range(len(a.children)):
                self.assertEqual(a, a.children[i].parent)
                _check(a.children[i], b.children[i])
        _check(root, expected)

    @staticmethod
    def build_test_tree(data):
        def _gen_tree(parent, s):
            # То есть это лист
            if type(s) is int:
                return TreeNode(s, parent, [])
            else:
                current = TreeNode(s[0], parent, [])
                for child in s[1]:
                    current.children.append(_gen_tree(current, child))
                return current
        return _gen_tree(None, data)

    def test_one_element(self):
        self.assertTreeEqual(build_tree([-1]),
                             BuildTreeTests.build_test_tree(0))

    def test_elements_in_row(self):
        self.assertTreeEqual(build_tree([-1, 0, 1]),
                             BuildTreeTests.build_test_tree((0, [(1, [2])])))

    def test_common(self):
        self.assertTreeEqual(build_tree([4, -1, 4, 1, 1]),
                             BuildTreeTests.build_test_tree((1,
                                                             [3, (4,
                                                                  [0, 2])
                                                              ]
                                                             )))


if __name__ == '__main__':
    unittest.main()
