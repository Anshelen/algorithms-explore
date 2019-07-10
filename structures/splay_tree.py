"""
Сплей-дерево - двоичное дерево поиска. Оно позволяет находить быстрее те данные,
которые использовались недавно. Все его основные операции выполняются в среднем
за логарифмическое время. По сравнению с АВЛ-деревьями проще реализуется.
"""

from typing import Optional, TypeVar, Generic, Tuple

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

    def __init__(self, key: K, value: V) -> None:
        self.key = key
        self.value = value
        self.right = None
        self.left = None
        self.parent = None

    def is_root(self) -> bool:
        """ Является ли узел корневым. """
        return self.parent is None

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

    def hang_to_parent(self, node: '_Node') -> None:
        """
        Подвешивает текущий узел к родителю переданного узла (node). Причем узел
        будет подвешен к родителю с той же стороны, что и node. Также, если
        родитель node отсутствует (корневой узел), то и текущий узел станет
        корневым.
        """
        parent = node.parent
        if node.is_left_child():
            parent.hang_left(self)
        elif node.is_right_child():
            parent.hang_right(self)
        else:
            self.parent = None

    def zigzig(self):
        """
                      b                      u
                     /  \                  /  \
                    a    d_sub        a_sub    a
                   /  \        ==>            /  \
                  u    c_sub             b_sub    b
                 /  \                            /  \
            a_sub    b_sub                  c_sub    d_sub

        a_sub < u < b_sub < a < c_sub < b < d_sub
        Должно применяться, если u узел 'u', и его родитель - оба являются
        левыми сыновьями.
        """
        u, a, b = self, self.parent, self.parent.parent
        a_sub, b_sub, c_sub, d_sub = u.left, u.right, a.right, b.right
        u.hang_to_parent(b)
        u.hang_left(a_sub)
        u.hang_right(a)
        a.hang_left(b_sub)
        a.hang_right(b)
        b.hang_left(c_sub)
        b.hang_right(d_sub)

    def zigzag(self):
        """
                  a                              u
                /  \                         /       \
           a_sub    b                     a             b
                   /  \        ==>      /   \         /   \
                  u    d_sub        a_sub  b_sub  c_sub   d_sub
                 /  \
            b_sub    c_sub

        a_sub < a < b_sub < u < c_sub < b < d_sub
        Должно применяться, если узел 'u' является левым сыном, а его родитель
        - правым.
        """
        u, b, a = self, self.parent, self.parent.parent
        a_sub, b_sub, c_sub, d_sub = a.left, u.left, u.right, b.right
        u.hang_to_parent(a)
        u.hang_left(a)
        u.hang_right(b)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        b.hang_left(c_sub)
        b.hang_right(d_sub)

    def zagzag(self):
        """
                   b                           u
                 /  \                         /  \
            a_sub    a                       a    d_sub
                   /  \        ==>          /  \
              b_sub    u                   b    c_sub
                      /  \                /  \
                 c_sub    d_sub      a_sub    b_sub

        a_sub < b < b_sub < a < c_sub < u < d_sub
        Должно применяться, если u узел 'u', и его родитель - оба являются
        правыми сыновьями.
        """
        u, a, b = self, self.parent, self.parent.parent
        a_sub, b_sub, c_sub, d_sub = b.left, a.left, u.left, u.right
        u.hang_to_parent(b)
        u.hang_left(a)
        u.hang_right(d_sub)
        a.hang_left(b)
        a.hang_right(c_sub)
        b.hang_left(a_sub)
        b.hang_right(b_sub)

    def zagzig(self):
        """
                  a                                u
                /   \                           /     \
               b     d_sub                  b             a
             /   \               ==>      /   \         /   \
        a_sub     u                   a_sub  b_sub  c_sub   d_sub
                /   \
            b_sub   c_sub

        a_sub < b < b_sub < u < c_sub < a < d_sub
        Должно применяться, если узел 'u' является правым сыном, а его родитель
        - левым.
        """
        u, b, a = self, self.parent, self.parent.parent
        a_sub, b_sub, c_sub, d_sub = b.left, u.left, u.right, a.right
        u.hang_to_parent(a)
        u.hang_left(b)
        u.hang_right(a)
        b.hang_left(a_sub)
        b.hang_right(b_sub)
        a.hang_left(c_sub)
        a.hang_right(d_sub)

    def zig(self) -> None:
        """
                  a                          u
                /   \                      /   \
              u      c_sub             a_sub     a
            /   \            ==>               /   \
        a_sub    b_sub                      b_sub  c_sub

        a_sub < u < b_sub < a < c_sub
        Должно применяться, если узел 'u' является левым сыном корня.
        """
        u, a = self, self.parent
        a_sub, b_sub, c_sub = u.left, u.right, a.right
        u.hang_right(a)
        u.hang_left(a_sub)
        a.hang_left(b_sub)
        a.hang_right(c_sub)
        u.parent = None

    def zag(self):
        """
              a                          u
            /   \                      /   \
        a_sub    u                    a    c_sub
                /  \       ==>      /   \
           b_sub    c_sub       a_sub   b_sub

        a_sub < a < b_sub < u < c_sub
        Должно применяться, если узел 'u' является правым сыном корня.
        """
        u, a = self, self.parent
        a_sub, b_sub, c_sub = a.left, u.left, u.right
        u.hang_left(a)
        u.hang_right(c_sub)
        a.hang_left(a_sub)
        a.hang_right(b_sub)
        u.parent = None


class SplayTreeMap(Generic[K, V]):
    """
    Коллекция, хранящая объекты в отсортированном по ключу порядке (в виде
    Сплей-дерева). Средняя сложность всех операций O(log n).
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
        new_node = self._new_node(key, value)
        if self.root is None:
            self.root = new_node
        else:
            def __inner(curr):
                if curr.key == key:
                    curr.value = value
                    self._splay(curr)
                elif curr.key > key:
                    if curr.left is None:
                        new_node.parent = curr
                        curr.left = new_node
                        self._splay(new_node)
                    else:
                        __inner(curr.left)
                else:
                    if curr.right is None:
                        new_node.parent = curr
                        curr.right = new_node
                        self._splay(new_node)
                    else:
                        __inner(curr.right)
            __inner(self.root)

    def __getitem__(self, item: K) -> V:
        """
        Получить значение по ключу. Если такого ключа в дереве нет, то бросает
        KeyError.
        """
        if not self:
            raise KeyError('Tree is empty')
        return self.find_node(item).value

    def _splay(self, node: _Node) -> None:
        """ Перемещает узел node в корень дерева попутно балансируя его.
        Выполняется за логарифмическое время в среднем. """
        if not node.parent:
            self.root = node
            return
        if not node.parent.parent:
            if node.is_left_child():
                node.zig()
            else:
                node.zag()
            self.root = node
        else:
            if node.is_left_child() and node.parent.is_left_child():
                node.zigzig()
            elif node.is_left_child() and node.parent.is_right_child():
                node.zigzag()
            elif node.is_right_child() and node.parent.is_right_child():
                node.zagzag()
            else:
                node.zagzig()
            self._splay(node)

    def find_node(self, key: K) -> '_Node':
        """ Находит узел дерева с переданным ключом в поддереве, либо
        возбуждает KeyError в случае отсутствия узла с таким ключом. """
        def __inner(curr):
            if curr.key == key:
                self._splay(curr)
                return curr
            elif curr.key > key:
                if curr.left is None:
                    self._splay(curr)
                    raise KeyError(f'No node with key: {key}')
                return __inner(curr.left)
            else:
                if curr.right is None:
                    self._splay(curr)
                    raise KeyError(f'No node with key: {key}')
                return __inner(curr.right)
        if not self:
            raise KeyError('Tree is empty')
        return __inner(self.root)

    def split(self, key: K) -> Tuple['SplayTreeMap', 'SplayTreeMap']:
        """
        Делит дерево на две части A и B по ключу key, такие что A <= key < B.
        Возвращает два отдельных дерева. После разделения исходное дерево не
        может быть использовано. Сложность O(log n).
        """
        if not self.root:
            return self.__class__(), self.__class__()

        def __inner(curr):
            if curr.key == key:
                self._splay(curr)
                return curr
            elif curr.key > key:
                if curr.left is None:
                    self._splay(curr)
                    return curr
                return __inner(curr.left)
            else:
                if curr.right is None:
                    self._splay(curr)
                    return curr
                return __inner(curr.right)
        node = __inner(self.root)
        if node.key <= key:
            right = node.unbind_right()
            return self.__class__(node), self.__class__(right)
        else:
            left = node.unbind_left()
            return self.__class__(left), self.__class__(node)

    def merge(self, b: 'SplayTreeMap') -> None:
        """ Сливает дерево b с текущим деревом. После слияния дерево b не должно
        использоваться напрямую. """
        if not self:
            self.root = b.root
            return
        if not b:
            return
        node = self.root.max_in_subtree()
        self._splay(node)
        node.hang_right(b.root)
        self.root = node

    def __delitem__(self, key: K) -> None:
        """
        Удаляет значение по ключу. Бросает KeyError, если такого ключа в дереве
        нет.
        """
        if not self:
            raise KeyError('Tree is empty')
        node = self.find_node(key)
        left = node.unbind_left()
        right = node.unbind_right()
        self.root = left
        self.merge(self.__class__(right))

    def __bool__(self) -> bool:
        return self.root is not None

    def __contains__(self, item: K) -> bool:
        try:
            if not self:
                return False
            self.find_node(item)
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
        node = self.find_node(key)
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
        node = self.find_node(key)
        if node.left is not None:
            return node.left.max_in_subtree().value
        else:
            while node.is_left_child():
                node = node.parent
            return node.parent.value if node.parent is not None else None

    # noinspection PyMethodMayBeStatic
    def _new_node(self, key: K, value: V) -> _Node:
        """ Создает новый узел. """
        return _Node(key, value)
