"""
АВЛ-дерево — сбалансированное по высоте двоичное дерево поиска: для каждой его
вершины высота её двух поддеревьев различается не более чем на 1. Все его
основные операции выполняются за логарифмическое время.
"""

from typing import Optional, TypeVar, Generic, Tuple

# Ключ и значение
K = TypeVar('K')
V = TypeVar('V')


class _Node(Generic[K, V]):
    """
    Узел дерева.
    """

    key: K
    value: V
    right: Optional["_Node"]
    left: Optional["_Node"]
    parent: Optional["_Node"]
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

    def hang_left(self, node: Optional["_Node"]) -> None:
        """ Подвесить переданный узел node к текущему узлу слева.
        Или отсоединить левый узел-потомок, если передать None. """
        self.left = node
        if node:
            node.parent = self

    def hang_right(self, node: Optional["_Node"]) -> None:
        """ Подвесить переданный узел node к текущему узлу справа.
        Или отсоединить правый узел-потомок, если передать None. """
        self.right = node
        if node:
            node.parent = self

    def update_invariants(self) -> None:
        """ Обновить параметры узла."""
        self.update_height()
        self.update_size()

    def update_height(self) -> None:
        """ Обновить параметр высоты узла. """
        l_height = self.left.height if self.left else 0
        r_height = self.right.height if self.right else 0
        self.height = max(l_height, r_height) + 1

    def update_size(self) -> None:
        """ Обновить количество элементов в узле. """
        l_size = self.left.size if self.left else 0
        r_size = self.right.size if self.right else 0
        self.size = l_size + r_size + 1

    def unbind_parent(self) -> None:
        """ Отсоединение узла от родителя. """
        if self.parent is None:
            return
        if self.parent.left == self:
            self.parent.left = None
        else:
            self.parent.right = None
        self.parent = None

    def unbind_left(self) -> Optional['_Node']:
        """
        Отсекает левого потомка, если он есть. По сути обособляет левое
        поддерево. Возвращает левого потомка или в случае его отсутствия -
        None.
        """
        child = self.left
        if child:
            child.unbind_parent()
            self.update_invariants()
        return child

    def unbind_right(self) -> Optional['_Node']:
        """
        Отсекает правого потомка, если он есть. По сути обособляет правое
        поддерево. Возвращает правого потомка или в случае его отсутствия -
        None.
        """
        child = self.right
        if child:
            child.unbind_parent()
            self.update_invariants()
        return child

    def max_in_subtree(self) -> '_Node':
        """ Находит узел с максимальном ключом в поддереве. """
        root = self
        while root.right is not None:
            root = root.right
        return root

    def min_in_subtree(self) -> '_Node':
        """ Находит узел с минимальным ключом в поддереве. """
        root = self
        while root.left is not None:
            root = root.left
        return root


def _swap(node1: _Node, node2: _Node) -> None:
    """ Обменять данные двух узлов (т.е. меняет ключи и значения узлов). """
    node1.key, node1.value, node2.key, node2.value \
        = node2.key, node2.value, node1.key, node1.value


class TreeMap(Generic[K, V]):
    """
    Коллекция, хранящая объекты в отсортированном по ключу порядке (в виде
    АВЛ-дерева). Сложность всех операций O(log n).
    """

    root: Optional[_Node]

    def __init__(self, root_node: _Node = None) -> None:
        """
        Создать дерево.

        :param root_node: корневой узел (для внутреннего использования)
        """
        self.root = root_node

    def __setitem__(self, key: K, value: V) -> None:
        """
        Помещает переданное значение value в дерево под ключом key. Если
        такой ключ уже существует, то значение этого узла будет перезаписано.
        """
        if self.root is None:
            self.root = self._new_node(key, value)

        def __inner(curr):
            if curr.key == key:
                curr.value = value
            elif curr.key > key:
                if curr.left is None:
                    new_node = self._new_node(key, value)
                    new_node.parent = curr
                    curr.left = new_node
                    self._repair(new_node)
                else:
                    __inner(curr.left)
            else:
                if curr.right is None:
                    new_node = self._new_node(key, value)
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
                    parent = node.parent
                    node.unbind_parent()
                    self._repair(parent)
            elif node.has_two_children():
                # Ищем максимальный элемент в левом поддереве
                el = node.left.max_in_subtree()
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

    def __contains__(self, item):
        try:
            self.__find_node(item)
            return True
        except KeyError:
            return False

    def max_key_value(self) -> V:
        """ Найти значение в дереве, соответствующее наибольшему ключу. """
        if not self:
            raise RuntimeError('Tree is empty')
        return self.root.max_in_subtree().value

    def min_key_value(self) -> V:
        """ Найти значение в дереве, соответствующее наименьшему ключу. """
        if not self:
            raise RuntimeError('Tree is empty')
        return self.root.min_in_subtree().value

    def next_key_value(self, key: K) -> V:
        """ Найти значение для ключа, следующего за переданным. """
        node = self.__find_node(key)
        if node.right is not None:
            return node.right.min_in_subtree().value
        else:
            while node.is_right_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    def prev_key_value(self, key: K) -> V:
        """ Найти значение для ключа, предыдущего за переданным. """
        node = self.__find_node(key)
        if node.left is not None:
            return node.left.max_in_subtree().value
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
        def __split(node: _Node):
            if node is None:
                return self.__class__(), self.__class__()
            node.unbind_parent()
            if node.is_leaf():
                if node.key <= key:
                    return self.__class__(node), self.__class__()
                else:
                    return self.__class__(), self.__class__(node)
            else:
                if node.key == key:
                    right = node.unbind_right()
                    return self.__class__(node), self.__class__(right)
                elif node.key > key:
                    left = node.unbind_left()
                    l1, l2 = __split(left)
                    l2.merge(self.__class__(node))
                    return l1, l2
                else:
                    right = node.unbind_right()
                    r1, r2 = __split(right)
                    left = self.__class__(node)
                    left.merge(r1)
                    return left, r2
        if not self.root:
            return self.__class__(), self.__class__()
        return __split(self.root)

    def merge(self, a: 'TreeMap') -> None:
        """
        Вливает дерево a в текущее дерево. Все элементы текущего дерева
        должны быть меньше, чем в дереве a. После слияния узлы сливаемого дерева
        становятся частью текущего дерева, поэтому дерево a не должно быть
        использовано впоследствии.
        Сложность алгоритма O(height(a) - height(b) + 1).
        """
        if not self:
            self.root = a.root
            return
        if not a:
            return

        # Элемент-разделитель
        mid = self.root.max_in_subtree()
        del self[mid.key]
        if not self:
            a[mid.key] = mid.value
            self.root = a.root
            return
        if self.root.height <= a.root.height + 1:
            mid.hang_right(a.root)
            mid.hang_left(self.root)
            mid.parent = None
            self.root = mid
        elif self.root.height > a.root.height:
            node = self.root
            while node.height > a.root.height + 1:
                node = node.right
            r = node.right
            node.hang_right(mid)
            mid.hang_right(a.root)
            mid.hang_left(r)
        else:
            node = a.root
            while node.height > a.root.height + 1:
                node = node.left
            r = node.left
            node.hang_left(mid)
            mid.hang_left(a.root)
            mid.hang_right(r)
            self.root = a.root
        self._repair(mid)

    def __find_node(self, key: K) -> _Node:
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

    @staticmethod
    def _new_node(key: K, value: V) -> _Node:
        """ Создает новый узел. """
        return _Node(key, value)

    def _repair(self, node: _Node) -> None:
        """ Восстановляет свойства дерева (его сбалансированность), начиная
        с переданного узла и рекурсивно до корня. """
        node.update_invariants()
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

    def __small_right_spin(self, node: _Node) -> None:
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
        a.update_invariants()
        b.update_invariants()

    def __small_left_spin(self, node: _Node) -> None:
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
        a.update_invariants()
        b.update_invariants()

    def __big_right_spin(self, node: _Node) -> None:
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
        a.update_invariants()
        b.update_invariants()
        c.update_invariants()

    def __big_left_spin(self, node: _Node) -> None:
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
        a.update_invariants()
        b.update_invariants()
        c.update_invariants()
