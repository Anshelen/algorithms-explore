import math
from io import StringIO


class Heap:
    """
    Очередь с приоритетами, представляющая собой двоичную мин-кучу. Для любой
    мин-кучи справедливы три условия:

    1. Значение в любой вершине не больше, чем значения её потомков.
    2. Глубина всех листьев отличается не более чем на 1 слой.
    3. Последний слой заполняется слева направо без «дырок».

    Скорость работы основных операций - вставки и извлечения минимума O(log n).
    Скорость создания массива - О(n).
    """

    def __init__(self, lst=None, prior_func=lambda x: x):
        """
        :param lst: начальный массив, который будет преобразован в кучу за
            линейное время
        :param prior_func: функция, позволяющая получить приоритет из элемента.
            Дефолтно приоритет равен самому элементу
        """
        self.prior_func = prior_func
        if lst:
            self.lst = lst
            for i in range(len(self.lst) // 2 - 1, -1, -1):
                self._shift_down(i)
        else:
            self.lst = []

    def insert(self, el):
        """
        Добавить элемент.
        """
        self.lst.append(el)
        self._shift_up(len(self) - 1)

    def extend(self, iterable):
        """
        Добавить все элементы из итерируемого объекта.
        """
        for el in iterable:
            self.insert(el)

    def remove(self, el):
        """
        Удалить элемент. Бросает ValueError, если элемент отсутствует.
        """
        index = self._index(el)
        if index == len(self) - 1:
            del self[index]
        else:
            self[index] = self[len(self) - 1]
            del self[len(self) - 1]
            self._shift_up(index)
            self._shift_down(index)

    def get_min(self):
        """
        Получить минимальный элемент из кучи. Бросает RuntimeError в случае,
        если куча пуста.
        """
        if not len(self):
            raise RuntimeError('Can not get minimum from empty heap')
        return self[0]

    def extract_min(self):
        """
        Извлечь минимальный элемент из кучи. Бросает RuntimeError в случае,
        если куча пуста.
        """
        res = self.get_min()
        self.remove(res)
        return res

    def _shift_up(self, index):
        """
        Осуществить попытку сдвинуть узел с переданным индексом вверх (ближе
        к корню).
        """
        if index == 0:
            return
        parent_index = (index - 1) // 2
        if self._priority(parent_index) > self._priority(index):
            self[index], self[parent_index] = self[parent_index], self[index]
            self._shift_up(parent_index)

    def _shift_down(self, index):
        """
        Осуществить попытку сдвинуть узел с переданным индексом вниз (ближе
        к листьям дерева).
        """
        indexes = [index] + self._get_children_indexes(index)
        min_index = min(indexes, key=lambda i: self._priority(i))
        if min_index != index:
            self[index], self[min_index] = self[min_index], self[index]
            self._shift_down(min_index)

    def _priority(self, index):
        return self.prior_func(self[index])

    def _get_children_indexes(self, index):
        children = []
        if self._has_left_child(index):
            children.append(2 * index + 1)
        if self._has_right_child(index):
            children.append(2 * index + 2)
        return children

    def _has_left_child(self, index):
        left_child_index = 2 * index + 1
        return left_child_index < len(self)

    def _has_right_child(self, index):
        right_child_index = 2 * index + 2
        return right_child_index < len(self)

    def _index(self, el, index=0):
        """
        Получить индекс элемента во внутреннем массиве. Поиск ведется в
        поддереве узла с индексом index.

        Args:
            el: искомый элемент
            index: индекс узла поддерева, в котором ведется поиск.

        Returns:
            Индекс элемента во внутреннем массиве дерева.

        Raises:
            ValueError: если такого элемента нет в дереве.
        """
        if not len(self):
            raise ValueError

        if self[index] == el:
            return index

        if self._priority(index) <= self.prior_func(el):
            # Поиск ведем "вглубь" дерева.
            try:
                l_child_index = 2 * index + 1
                if self._has_left_child(index):
                    return self._index(el, l_child_index)
            except ValueError:
                r_child_index = 2 * index + 2
                if self._has_right_child(index):
                    return self._index(el, r_child_index)
        raise ValueError

    def __getitem__(self, item):
        return self.lst.__getitem__(item)

    def __setitem__(self, key, value):
        return self.lst.__setitem__(key, value)

    def __delitem__(self, key):
        return self.lst.__delitem__(key)

    def __str__(self):
        total_width = 36
        output = StringIO()
        last_row = -1
        for i, n in enumerate(self.lst):
            if i:
                row = int(math.floor(math.log(i + 1, 2)))
            else:
                row = 0
            if row != last_row:
                output.write('\n')
            columns = 2 ** row
            col_width = int(math.floor(total_width / columns))
            output.write(str(n).center(col_width, ' '))
            last_row = row
        output.write('\n')
        output.write('-' * total_width)
        output.write('\n')
        return output.getvalue()

    def __len__(self):
        return self.lst.__len__()
