from typing import Tuple, Optional

from structures.avl_tree import _Node, K, V, TreeMap


class _NoKeyNode(_Node):
    """ Узел дерева с неявными ключами. """

    def put(self, new_node: '_NoKeyNode') -> None:
        """ Помещает новый узел в поддерево. Новый узел всегда будет
        максимальным в поддереве. """
        def __inner(curr):
                if curr.right is None:
                    curr.hang_right(new_node)
                    curr.repair()
                else:
                    __inner(curr.right)
        __inner(self)

    @staticmethod
    def merge_with_root(a: Optional['_NoKeyNode'], b: Optional['_NoKeyNode'],
                        t: '_NoKeyNode') -> '_NoKeyNode':
        t.update_invariants()
        t.clear_relations()
        if a is None and b is None:
            return t
        if a is None:
            min_el = b.min_in_subtree()
            min_el.hang_left(t)
            min_el.repair()
            return b
        if b is None:
            a.put(t)
            return a
        a.unbind_parent()
        b.unbind_parent()

        if abs(a.height - b.height) <= 1:
            t.hang_right(b)
            t.hang_left(a)
            t.update_invariants()
            return t
        elif a.height > b.height:
            t_new = _NoKeyNode.merge_with_root(a.right, b, t)
            a.hang_right(t_new)
            t_new.repair()
            return a
        else:
            t_new = _NoKeyNode.merge_with_root(a, b.left, t)
            b.hang_left(t_new)
            t_new.repair()
            return b


class _NoKeyTreeMap(TreeMap):
    """
    Дерево поиска с неявными ключами.
    """

    def _new_node(self, key: K, value: V) -> _NoKeyNode:
        return _NoKeyNode(key, value)

    def merge(self, b: '_NoKeyTreeMap') -> None:
        if not self:
            self.root = b.root
            return
        if not b:
            return

        # Элемент-разделитель
        mid = self.root.max_in_subtree()
        if len(self) == 1:
            min_el = b.root.min_in_subtree()
            min_el.hang_left(mid)
            min_el.repair()
            self.root = b.root
            return

        parent = mid.parent
        if parent:
            mid.unbind_parent()
            parent.hang_right(mid.left)
            parent.repair()
        else:
            self.root = mid.left

        t = _NoKeyNode.merge_with_root(self.root, b.root, mid)
        self.root = t

    def split(self, i: K) -> Tuple['_NoKeyTreeMap', '_NoKeyTreeMap']:
        """
        Делит дерево на две части A и B по индексу i так, что все элементы
        от 0 до i включительно будут в дереве A, а остальные в B. Возвращает два
        отдельных сбалансированных дерева. После разделения исходное дерево
        не может быть использовано. Сложность O(log n).
        """
        def __split(node: _Node, i):
            if node is None:
                return None, None
            node.unbind_parent()
            l_size = node.left.size if node.left else 0
            if l_size == i:
                right = node.unbind_right()
                if node.left:
                    left = node.unbind_left()
                    node.update_invariants()
                    left.put(node)
                    return left, right
                else:
                    return node, right
            if l_size < i:
                r1, r2 = __split(node.right, i - l_size - 1)
                left_child = node.left
                if left_child is not None:
                    node.left.unbind_parent()
                node.update_invariants()
                left = _NoKeyNode.merge_with_root(left_child, r1, node)
                return left, r2
            else:
                l1, l2 = __split(node.left, i)
                right_child = node.right
                if right_child:
                    right_child.unbind_parent()
                node.update_invariants()
                right = _NoKeyNode.merge_with_root(l2, right_child, node)
                return l1, right

        if not self.root:
            return _NoKeyTreeMap(), _NoKeyTreeMap()
        a, b = __split(self.root, i)
        if a:
            a.parent = None
        if b:
            b.parent = None
        return _NoKeyTreeMap(a), _NoKeyTreeMap(b)


class CharSet:
    """
    Структура, принимающая на вход строку и позволяющая за логарифмическое время
    выполнять две основные операции:
        1. Искать символ по индексу
        2. Переставить две части строки слева и справа от индекса
    Основана на дереве поиска с неявными ключами.
    """

    def __init__(self, s: str = None):
        self.map = _NoKeyTreeMap()
        if not s:
            return
        self.map[None] = s[0]
        for i in range(1, len(s)):
            sec = CharSet(s[i])
            self.map.merge(sec.map)

    def __getitem__(self, i: int) -> str:
        """ Получить символ по индексу. """
        return self.map.get_by_index(i)

    def swap(self, i: int) -> None:
        """
        Переставить подстроки с индексами в интервале [0, i] и (i, len(s))
        местами. То есть из строки 'abcd' при индексе i = 1 получится 'cdab'.
        """
        if i < 0 or i >= len(self):
            raise IndexError
        a, b = self.map.split(i)
        b.merge(a)
        self.map = b

    def __str__(self) -> str:
        res = [self.__getitem__(i) for i in range(len(self.map))]
        return ''.join(res)

    def __len__(self):
        return len(self.map)

    def __bool__(self):
        return bool(self.map)
