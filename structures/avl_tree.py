"""
АВЛ-дерево — сбалансированное по высоте двоичное дерево поиска: для каждой его
вершины высота её двух поддеревьев различается не более чем на 1. Все его
основные операции выполняются за логарифмическое время.
"""

from typing import Optional, TypeVar, Generic, Tuple

# Ключ и значение
K = TypeVar('K')
V = TypeVar('V')


class Node(Generic[K, V]):
    """
    Узел дерева.
    """

    key: K
    value: V
    right: Optional["Node"]
    left: Optional["Node"]
    parent: Optional["Node"]
    height: int
    size: int

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.right = None
        self.left = None
        self.parent = None
        self.height = 1
        self.size = 1

    def unbind_parent(self) -> None:
        """ Отсоединение узла от родителя. """
        if self.parent is None:
            return
        if self.parent.left == self:
            self.parent.left = None
        else:
            self.parent.right = None

    def is_root(self) -> bool:
        """ Является ли узел корневым. """
        return self.parent is None

    def is_leaf(self) -> bool:
        """ Является ли узел листовым. """
        return self.left is None and self.right is None

    def has_two_children(self) -> bool:
        """ Имеет ли узел два узла-потомка. """
        return self.left is not None and self.right is not None

    def has_one_children(self) -> bool:
        """ Имеет ли узел только один узел-потомок. """
        return not self.is_leaf() and not self.has_two_children()

    def is_left_child(self) -> bool:
        """ Является ли узел левым ребенком своего родителя.
        Если узел корневой, то вернет false. """
        if self.is_root():
            return False
        return self.parent.left == self

    def is_right_child(self) -> bool:
        """ Является ли узел правым ребенком своего родителя.
        Если узел корневой, то вернет false. """
        if self.is_root():
            return False
        return self.parent.right == self

    def hang_left(self, node: Optional["Node"]) -> None:
        """ Подвесить переданный узел node к текущему узлу слева.
        Или отсоединить левый узел-потомок, если передать None. """
        self.left = node
        if node:
            node.parent = self

    def hang_right(self, node: Optional["Node"]) -> None:
        """ Подвесить переданный узел node к текущему узлу справа.
        Или отсоединить правый узел-потомок, если передать None. """
        self.right = node
        if node:
            node.parent = self


def _split_left(node: Node) -> Tuple[Optional['Node'], Optional['Node']]:
    """
    Отсекает левого потомка, если он есть. По сути обособляет левое
    поддерево. Возвращает кортеж из двух узлов - левого потомка и
    переданного узла. В случае отсутствия потомка вернет None.
    """
    child = node.left
    if child:
        child.parent = None
    node.left = None
    _update_invariants(node)
    return child, node


def _split_right(node: Node) -> Tuple[Optional['Node'], Optional['Node']]:
    """
    Отсекает правого потомка, если он есть. По сути обособляет правое
    поддерево. Возвращает кортеж из двух узлов - переданного узла и правого
    потомка. В случае отсутствия потомка вернет None.
    """
    child = node.right
    if child:
        child.parent = None
    node.right = None
    _update_invariants(node)
    return node, child


def _update_invariants(node: Node) -> None:
    """ Обновить параметры узла: высоту поддерева и его количество элементов."""
    _update_height(node)
    _update_size(node)


def _update_height(node: Node) -> None:
    """ Обновить параметр высоты узла. """
    l_height = node.left.height if node.left else 0
    r_height = node.right.height if node.right else 0
    node.height = max(l_height, r_height) + 1


def _update_size(node: Node) -> None:
    """ Обновить количество элементов в поддереве. """
    l_size = node.left.size if node.left else 0
    r_size = node.right.size if node.right else 0
    node.size = l_size + r_size + 1


def _swap(node1: Node, node2: Node) -> None:
    """ Обменять данные двух узлов (т.е. меняет ключи и значения узлов). """
    node1.key, node1.value, node2.key, node2.value \
        = node2.key, node2.value, node1.key, node1.value


def _max_in_subtree(root: Node) -> Node:
    """ Находит узел с максимальном ключом в поддереве с переданным корнем. """
    while root.right is not None:
        root = root.right
    return root


def _min_in_subtree(root: Node) -> Node:
    """ Находит узел с минимальным ключом в поддереве с переданным корнем. """
    while root.left is not None:
        root = root.left
    return root


class TreeMap(Generic[K, V]):
    """
    Коллекция, хранящая объекты в отсортированном по ключу порядке (в виде
    АВЛ-дерева). Сложность всех операций O(log n).
    """

    root: Optional[Node]

    def __init__(self) -> None:
        self.root = None

    def __setitem__(self, key: K, value: V) -> None:
        """
        Помещает переданное значение value в дерево под ключом key. Если
        такой ключ уже существует, то значение этого узла будет перезаписано.
        """
        if self.root is None:
            self.root = Node(key, value)

        def __inner(curr):
            if curr.key == key:
                curr.value = value
            elif curr.key > key:
                if curr.left is None:
                    new_node = Node(key, value)
                    new_node.parent = curr
                    curr.left = new_node
                    self._repair(new_node)
                else:
                    __inner(curr.left)
            else:
                if curr.right is None:
                    new_node = Node(key, value)
                    new_node.parent = curr
                    curr.right = new_node
                    self._repair(new_node)
                else:
                    __inner(curr.right)

        __inner(self.root)

    def __getitem__(self, item: K) -> V:
        """
        Получить значение по ключу. Если такого ключа в дереве нет, то бросает
        KeyError.
        """
        return self.__find_node(item).value

    def __delitem__(self, key: K) -> None:
        """
        Удаляет значение по ключу. Бросает KeyError, если такого ключа в дереве
        нет.
        """

        def __delete_node(node):
            if node.is_leaf():
                if node.is_root():
                    self.root = None
                else:
                    node.unbind_parent()
                    self._repair(node)
            elif node.has_two_children():
                # Ищем максимальный элемент в левом поддереве
                el = _max_in_subtree(node.left)
                _swap(node, el)
                __delete_node(el)
                self._repair(el)
            else:  # Один потомок
                child = node.left if node.left else node.right
                if node.is_root():
                    child.parent = None
                    self.root = child
                else:
                    child.parent = node.parent
                    if node.is_left_child():
                        node.parent.left = child
                    else:
                        node.parent.right = child
                    self._repair(child)

        node = self.__find_node(key)
        __delete_node(node)

    def __len__(self):
        return self.root.size if self.root else 0

    def __bool__(self):
        return self.__len__() > 0

    def max_key_value(self) -> V:
        """ Найти значение в дереве, соответствующее наибольшему ключу. """
        if self.root is None:
            raise RuntimeError('Tree is empty')
        return _max_in_subtree(self.root).value

    def min_key_value(self) -> V:
        """ Найти значение в дереве, соответствующее наименьшему ключу. """
        if self.root is None:
            raise RuntimeError('Tree is empty')
        return _min_in_subtree(self.root).value

    def next_key_value(self, key: K) -> V:
        """ Найти значение для ключа, следующего за переданным. """
        node = self.__find_node(key)
        if node.right is not None:
            return _min_in_subtree(node.right).value
        else:
            while node.is_right_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    def prev_key_value(self, key: K) -> V:
        """ Найти значение для ключа, предыдущего за переданным. """
        node = self.__find_node(key)
        if node.left is not None:
            return _max_in_subtree(node.left).value
        else:
            while node.is_left_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    def get_by_index(self, i: int) -> V:
        """ Получить значение, соответствующее i-ому ключу в дереве. """
        if i > len(self) - 1 or i < 0:
            raise IndexError('tree index out of range')

        def __inner_get(node, i):
            l_size = node.left.size if node.left else 0
            if l_size == i:
                return node.value
            elif l_size > i:
                return __inner_get(node.left, i)
            else:
                return __inner_get(node.right, i - l_size - 1)
        return __inner_get(self.root, i)

    def split(self, key: K) -> Tuple['TreeMap', 'TreeMap']:
        """
        Делит дерево на две части A и B по ключу key, такие что A <= key < B.
        Возвращает два отдельных дерева. После разделения исходное дерево не
        может быть использовано. Сложность O(log n).
        """
        def __split(node: Node):
            if node is None:
                return TreeMap(), TreeMap()
            if node.is_leaf():
                if node.key <= key:
                    return TreeMap.__from(node), TreeMap()
                else:
                    return TreeMap(), TreeMap.__from(node)
            else:
                if node.key == key:
                    left, right = _split_right(node)
                    return TreeMap.__from(left), TreeMap.__from(right)
                elif node.key > key:
                    left, right = _split_left(node)
                    l1, l2 = __split(left)
                    return l1, TreeMap.merge(l2, TreeMap.__from(right))
                else:
                    left, right = _split_right(node)
                    r1, r2 = __split(right)
                    return TreeMap.merge(TreeMap.__from(left), r1), r2
        if not self.root:
            return TreeMap(), TreeMap()
        return __split(self.root)

    @staticmethod
    def merge(a: 'TreeMap', b: 'TreeMap') -> 'TreeMap':
        """
        Сливает два дерева и возвращает новое дерево. Все элементы дерева a
        должны быть меньше, чем в дереве b. После слияния первоначальные
        деревья не должны быть использованы.
        Сложность алгоритма O(height(a) - height(b) + 1).
        """
        if not a:
            return b
        if not b:
            return a

        # Элемент-разделитель
        mid = _max_in_subtree(a.root)
        del a[mid.key]
        if not a:
            b[mid.key] = mid.value
            return b
        res = TreeMap()
        if a.root.height <= b.root.height + 1:
            mid.hang_right(b.root)
            mid.hang_left(a.root)
            mid.parent = None
            res.root = mid
        elif a.root.height > b.root.height:
            node = a.root
            while node.height > b.root.height + 1:
                node = node.right
            r = node.right
            node.hang_right(mid)
            mid.hang_right(b.root)
            mid.hang_left(r)
            res.root = a.root
        else:
            node = b.root
            while node.height > b.root.height + 1:
                node = node.left
            r = node.left
            node.hang_left(mid)
            mid.hang_left(b.root)
            mid.hang_right(r)
            res.root = b.root
        res._repair(mid)
        return res

    @staticmethod
    def __from(node: Optional[Node]):
        """ Создает дерево из узла. При этом отсекает его от родителя. Если
        вместо узла передан None, то создаст пустое дерево. """
        res = TreeMap()
        if node:
            node.unbind_parent()
            node.parent = None
        res.root = node
        return res

    def __find_node(self, key: K) -> Node:
        """ Находит узел дерева с переданным ключом, либо возбуждает KeyError в
        случае отсутствия узла с таким ключом. """

        def __inner(curr):
            if curr.key == key:
                return curr
            elif curr.key > key:
                if curr.left is None:
                    raise KeyError(f'No node with key: {key}')
                return __inner(curr.left)
            else:
                if curr.right is None:
                    raise KeyError(f'No node with key: {key}')
                return __inner(curr.right)

        if not self.root:
            raise KeyError(f'No node with key: {key}')
        return __inner(self.root)

    def _repair(self, node: Node) -> None:
        """ Восстановляет свойства дерева (его сбалансированность), начиная
        с переданного узла и рекурсивно до корня. """
        _update_invariants(node)
        r_height = node.right.height if node.right else 0
        l_height = node.left.height if node.left else 0
        if abs(r_height - l_height) == 2:
            r_r_height = node.right.right.height \
                if node.right and node.right.right else 0
            r_l_height = node.right.left.height \
                if node.right and node.right.left else 0
            l_l_height = node.left.left.height \
                if node.left and node.left.left else 0
            l_r_height = node.left.right.height \
                if node.left and node.left.right else 0
            if l_height < r_r_height:
                self.__small_right_spin(node)
            elif l_height < r_l_height:
                self.__big_right_spin(node)
            elif r_height < l_l_height:
                self.__small_left_spin(node)
            elif r_height < l_r_height:
                self.__big_left_spin(node)
            else:
                raise RuntimeError('Not expected error')
        if node.parent:
            self._repair(node.parent)

    def __small_right_spin(self, node: Node) -> None:
        """ Осуществляет малое правое вращение в переданном узле.

              a                           b
            /   \                       /   \
        a_sub     b                    a    c_sub
                 /  \       ==>      /   \
            b_sub    c_sub        a_sub  b_sub

        a_sub < a < b_sub < b < c_sub
        Должно применяться, если высота поддерева a_sub меньше, чем c_sub.
        """
        parent, a, b = node.parent, node, node.right
        a_sub, b_sub, c_sub = node.left, node.right.left, node.right.right
        if a.is_left_child():
            parent.hang_left(b)
        elif a.is_right_child():
            parent.hang_right(b)
        else:
            self.root = b
            b.parent = None
        b.hang_left(a)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        b.hang_right(c_sub)
        _update_invariants(a)
        _update_invariants(b)

    def __small_left_spin(self, node: Node) -> None:
        """ Осуществляет малое левое вращение в переданном узле.

                  a                          b
                /   \                      /   \
              b      c_sub             a_sub     a
            /   \            ==>               /   \
        a_sub    b_sub                      b_sub  c_sub

        a_sub < b < b_sub < a < c_sub
        Должно применяться, если высота поддерева c_sub меньше, чем a_sub.
        """
        parent, a, b = node.parent, node, node.left
        a_sub, b_sub, c_sub = node.left.left, node.left.right, node.right
        if a.is_left_child():
            parent.hang_left(b)
        elif a.is_right_child():
            parent.hang_right(b)
        else:
            self.root = b
            b.parent = None
        b.hang_right(a)
        b.hang_left(a_sub)
        a.hang_left(b_sub)
        a.hang_right(c_sub)
        _update_invariants(a)
        _update_invariants(b)

    def __big_right_spin(self, node: Node) -> None:
        """ Осуществляет большое правое вращение в переданном узле.

              a                               c
            /   \                           /   \
        a_sub     b                    a             b
                 /  \          ==>   /   \         /   \
                c    d_sub        a_sub  b_sub   c_sub  d_sub
              /   \
            b_sub  c_sub

        a_sub < a < b_sub < c < c_sub < b < d_sub
        Должно применяться, если высота поддерева a_sub меньше, чем высота узла
        c.
        """
        parent, a, b, c = node.parent, node, node.right, node.right.left
        a_sub, b_sub, c_sub, d_sub = node.left, node.right.left.left, \
                                     node.right.left.right, node.right.right
        if a.is_left_child():
            parent.hang_left(c)
        elif a.is_right_child():
            parent.hang_right(c)
        else:
            self.root = c
            c.parent = None
        c.hang_left(a)
        c.hang_right(b)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        b.hang_left(c_sub)
        b.hang_right(d_sub)
        _update_invariants(a)
        _update_invariants(b)
        _update_invariants(c)

    def __big_left_spin(self, node: Node) -> None:
        """ Осуществляет большое левое вращение в переданном узле.

                  a                             c
                /   \                         /   \
              b       d_sub              b             a
            /   \            ==>       /   \         /   \
        a_sub     c                a_sub  b_sub  c_sub  d_sub
                /   \
             b_sub  c_sub

        a_sub < b < b_sub < c < c_sub < a < d_sub
        Должно применяться, если высота поддерева d_sub меньше, чем высота узла
        c.
        """
        parent, a, b, c = node.parent, node, node.left, node.left.right
        a_sub, b_sub, c_sub, d_sub = node.left.left, node.left.right.left, \
                                     node.left.right.right, node.right
        if a.is_left_child():
            parent.hang_left(c)
        elif a.is_right_child():
            parent.hang_right(c)
        else:
            self.root = c
            c.parent = None
        c.hang_left(b)
        c.hang_right(a)
        b.hang_left(a_sub)
        b.hang_right(b_sub)
        a.hang_left(c_sub)
        a.hang_right(d_sub)
        _update_invariants(a)
        _update_invariants(b)
        _update_invariants(c)
