"""
АВЛ-дерево — сбалансированное по высоте двоичное дерево поиска: для каждой его
вершины высота её двух поддеревьев различается не более чем на 1. Все его
основные операции выполняются за логарифмическое время.
"""

from typing import Optional, TypeVar, Generic, Tuple, Sequence, Any

# Ключ и значение
K = TypeVar('K')
V = TypeVar('V')


class _Node(Generic[K, V]):
    """
    Узел дерева. Отражает поддерево.
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

    def put(self, new_node: '_Node') -> None:
        """
        Помещает новый узел в поддерево. Если уже существует узел с тем же
        ключом, то значение этого узла будет перезаписано.
        """
        key, value = new_node.key, new_node.value

        def __inner(curr):
            if curr.key == key:
                curr.value = value
            elif curr.key > key:
                if curr.left is None:
                    new_node.parent = curr
                    curr.left = new_node
                    curr.repair()
                else:
                    __inner(curr.left)
            else:
                if curr.right is None:
                    new_node.parent = curr
                    curr.right = new_node
                    curr.repair()
                else:
                    __inner(curr.right)
        __inner(self)

    def repair(self) -> None:
        """ Восстановляет свойства дерева (его сбалансированность), начиная
        с текущего узла и рекурсивно до корня. """
        self.update_invariants()
        r_height = self.right.height if self.right else 0
        l_height = self.left.height if self.left else 0
        if abs(r_height - l_height) == 2:
            r_r_height = self.right.right.height \
                if self.right and self.right.right else 0
            r_l_height = self.right.left.height \
                if self.right and self.right.left else 0
            l_l_height = self.left.left.height \
                if self.left and self.left.left else 0
            l_r_height = self.left.right.height \
                if self.left and self.left.right else 0
            if l_height < r_r_height:
                self.__small_right_spin()
            elif l_height < r_l_height:
                self.__big_right_spin()
            elif r_height < l_l_height:
                self.__small_left_spin()
            elif r_height < l_r_height:
                self.__big_left_spin()
            else:
                raise RuntimeError('Not expected error')
        if self.parent:
            self.parent.repair()

    def get_by_index(self, i: int) -> V:
        """ Получить значение, соответствующее i-ому ключу в поддереве. """
        if i > self.size - 1 or i < 0:
            raise IndexError('tree index out of range')

        def __get(node, i):
            l_size = node.left.size if node.left else 0
            if l_size == i:
                return node.value
            elif l_size > i:
                return __get(node.left, i)
            else:
                return __get(node.right, i - l_size - 1)
        return __get(self, i)

    def __small_right_spin(self) -> None:
        """ Осуществляет малое правое вращение в переданном узле.

              a                           b
            /   \                       /   \
        a_sub     b                    a    c_sub
                 /  \       ==>      /   \
            b_sub    c_sub        a_sub  b_sub

        a_sub < a < b_sub < b < c_sub
        Должно применяться, если высота поддерева a_sub меньше, чем c_sub.
        """
        parent, a, b = self.parent, self, self.right
        a_sub, b_sub, c_sub = self.left, self.right.left, self.right.right
        _swap(a, b)
        a, b = b, a
        b.hang_left(a)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        b.hang_right(c_sub)
        a.update_invariants()
        b.update_invariants()

    def __small_left_spin(self) -> None:
        """ Осуществляет малое левое вращение в переданном узле.

                  a                          b
                /   \                      /   \
              b      c_sub             a_sub     a
            /   \            ==>               /   \
        a_sub    b_sub                      b_sub  c_sub

        a_sub < b < b_sub < a < c_sub
        Должно применяться, если высота поддерева c_sub меньше, чем a_sub.
        """
        parent, a, b = self.parent, self, self.left
        a_sub, b_sub, c_sub = self.left.left, self.left.right, self.right
        _swap(a, b)
        a, b = b, a
        b.hang_right(a)
        b.hang_left(a_sub)
        a.hang_left(b_sub)
        a.hang_right(c_sub)
        a.update_invariants()
        b.update_invariants()

    def __big_right_spin(self) -> None:
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
        parent, a, b, c = self.parent, self, self.right, self.right.left
        a_sub, b_sub, c_sub, d_sub = self.left, self.right.left.left, \
                                     self.right.left.right, self.right.right
        _swap(a, c)
        a, c = c, a
        c.hang_left(a)
        c.hang_right(b)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        b.hang_left(c_sub)
        b.hang_right(d_sub)
        a.update_invariants()
        b.update_invariants()
        c.update_invariants()

    def __big_left_spin(self) -> None:
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
        parent, a, b, c = self.parent, self, self.left, self.left.right
        a_sub, b_sub, c_sub, d_sub = self.left.left, self.left.right.left, \
                                     self.left.right.right, self.right
        _swap(a, c)
        a, c = c, a
        c.hang_left(b)
        c.hang_right(a)
        b.hang_left(a_sub)
        b.hang_right(b_sub)
        a.hang_left(c_sub)
        a.hang_right(d_sub)
        a.update_invariants()
        b.update_invariants()
        c.update_invariants()

    def find_node(self, key: K) -> '_Node':
        """ Находит узел дерева с переданным ключом в поддереве, либо
        возбуждает KeyError в случае отсутствия узла с таким ключом. """

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
        return __inner(self)

    def clear_relations(self):
        """ Удаляет ссылки на родителя и потомков. """
        self.parent = None
        self.left = None
        self.right = None


def _swap(node1: _Node, node2: _Node) -> None:
    """ Обменять данные двух узлов (т.е. меняет ключи и значения узлов). """
    node1.key, node1.value, node2.key, node2.value \
        = node2.key, node2.value, node1.key, node1.value


def _merge_with_root(a: Optional[_Node], b: Optional[_Node], t: _Node) -> _Node:
    """
    Осуществляет слияние поддеревьев с корнями a и b при среднем элементе t.
    Причем для всех элементов справедливо a < t < b. Переменные a и b могут
    иметь значение None. Возвращает корень объединенного дерева.
    """
    t.update_invariants()
    t.clear_relations()
    if a is None and b is None:
        return t
    if a is None:
        b.put(t)
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
        t_new = _merge_with_root(a.right, b, t)
        a.hang_right(t_new)
        t_new.repair()
        return a
    else:
        t_new = _merge_with_root(a, b.left, t)
        b.hang_left(t_new)
        t_new.repair()
        return b


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
        else:
            self.root.put(self._new_node(key, value))

    def __getitem__(self, item: K) -> V:
        """
        Получить значение по ключу. Если такого ключа в дереве нет, то бросает
        KeyError.
        """
        if not self:
            raise KeyError('Tree is empty')
        return self.root.find_node(item).value

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
                    parent.repair()
            elif node.has_two_children():
                # Ищем максимальный элемент в левом поддереве
                el = node.left.max_in_subtree()
                _swap(node, el)
                __delete_node(el)
                el.repair()
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
                    child.repair()
        if not self:
            raise KeyError('Tree is empty')
        node = self.root.find_node(key)
        __delete_node(node)

    def __len__(self):
        return self.root.size if self.root else 0

    def __bool__(self):
        return self.__len__() > 0

    def __contains__(self, item):
        try:
            if not self:
                return False
            self.root.find_node(item)
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
        if not self:
            raise KeyError('Tree is empty')
        node = self.root.find_node(key)
        if node.right is not None:
            return node.right.min_in_subtree().value
        else:
            while node.is_right_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    def prev_key_value(self, key: K) -> V:
        """ Найти значение для ключа, предыдущего за переданным. """
        if not self:
            raise KeyError('Tree is empty')
        node = self.root.find_node(key)
        if node.left is not None:
            return node.left.max_in_subtree().value
        else:
            while node.is_left_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    def get_by_index(self, i: int) -> V:
        """ Получить значение, соответствующее i-ому ключу в дереве. """
        if not self:
            raise IndexError('tree index out of range')
        return self.root.get_by_index(i)

    def split(self, key: K) -> Tuple['TreeMap', 'TreeMap']:
        """
        Делит дерево на две части A и B по ключу key, такие что A <= key < B.
        Возвращает два отдельных дерева. После разделения исходное дерево не
        может быть использовано. Сложность O(log n).
        """
        def __split(node: _Node):
            if node is None:
                return None, None
            node.unbind_parent()
            if node.key > key:
                l1, l2 = __split(node.left)
                right_child = node.right
                if right_child:
                    node.right.unbind_parent()
                right = _merge_with_root(l2, right_child, node)
                return l1, right
            else:
                r1, r2 = __split(node.right)
                left_child = node.left
                if left_child:
                    node.left.unbind_parent()
                left = _merge_with_root(left_child, r1, node)
                return left, r2
        if not self.root:
            return self.__class__(), self.__class__()
        a, b = __split(self.root)
        if a:
            a.parent = None
        if b:
            b.parent = None
        return self.__class__(a), self.__class__(b)

    def merge(self, b: 'TreeMap') -> None:
        """ Сливает дерево b с текущим деревом. После слияния дерево b не должно
        использоваться напрямую. """
        if not self:
            self.root = b.root
            return
        if not b:
            return

        # Элемент-разделитель
        mid = self.root.max_in_subtree()
        del self[mid.key]
        if not self:
            b[mid.key] = mid.value
            self.root = b.root
            return
        t = _merge_with_root(self.root, b.root, mid)
        self.root = t

    def _new_node(self, key: K, value: V) -> _Node:
        """ Создает новый узел. """
        return _Node(key, value)


class TreeSet:
    """
    Реализация множества на основе АВЛ-дерева.
    """

    def __init__(self, m: 'TreeMap' = None, keys: Sequence[Any] = None) -> None:
        """
        Создать множество на основе АВЛ-дерева.

        :param m: АВЛ-дерево (если не указано, то будет создано стандартное
        дерево). Дерево должно содержать пары "ключ => ключ".
        :param keys: массив ключей дерева
        """
        if m is None:
            m = TreeMap()
        self.map = m
        for key in (keys or []):
            self.put(key)
        self.map._new_node = self._new_node()

    def _new_node(self):
        return self.map._new_node

    def put(self, key: Any) -> None:
        """ Поместить ключ в дерево. """
        self.map[key] = key

    def get(self, i: int) -> Any:
        """ Получить i-ый ключ. """
        return self.map.get_by_index(i)

    def delete(self, key: Any) -> None:
        """ Удалить ключ из дерева. """
        del self.map[key]

    def max(self) -> Any:
        """ Максимальный ключ в множестве. """
        return self.map.max_key_value()

    def min(self) -> Any:
        """ Минимальный ключ в множестве. """
        return self.map.min_key_value()

    def next(self, key: Any) -> Any:
        """ Следующий ключ в множестве. """
        return self.map.next_key_value(key)

    def prev(self, key: Any) -> Any:
        """ Предыдущий ключ в множестве. """
        return self.map.prev_key_value(key)

    def split(self, key: Any) -> Tuple['TreeSet', 'TreeSet']:
        a, b = self.map.split(key)
        return self.__class__(a), self.__class__(b)

    def merge(self, b: 'TreeSet') -> None:
        self.map.merge(b.map)

    def __len__(self):
        return self.map.__len__()

    def __bool__(self):
        return self.map.__bool__()

    def __contains__(self, item):
        return self.map.__contains__(item)
