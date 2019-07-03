"""
Множество на основе АВЛ-дерева, позволяющая за логарифмическое время найти сумму
всех ключей из определенного интервала.
"""

from structures.avl_tree import _Node, TreeSet, K, V


class _SumNode(_Node):
    """
    Узел дерева, содержащий сумму ключей узлов поддеревьев.
    """

    def __init__(self, key: int) -> None:
        super().__init__(key, key)
        self.sum = key

    def _update_sum(self) -> None:
        """ Обновить сумму ключей в поддереве. """
        l_sum = self.left.sum if self.left else 0
        r_sum = self.right.sum if self.right else 0
        self.sum = l_sum + r_sum + self.key

    def update_invariants(self) -> None:
        super().update_invariants()
        self._update_sum()


class SumTreeSet(TreeSet):

    def _new_node(self):
        def __inner(key: K, value: V) -> _Node:
            return _SumNode(key)
        return __inner

    def get_sum(self):
        """
        Получить сумму всех ключей множества.
        """
        if not self.map.root:
            return 0
        return self.map.root.sum

    def subset_sum(self, k1: int, k2: int) -> int:
        """
        Получить сумму всех ключей множества из интервала [k1, k2]
        """
        if k1 > k2:
            raise IndexError('Invalid indexes')
        center, right = self.split(k2)
        left, center = center.split(k1 - 1)
        res = center.get_sum() if center else 0
        left.merge(center)
        left.merge(right)
        self.map.root = left.map.root
        return res
