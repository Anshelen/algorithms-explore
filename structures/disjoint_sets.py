"""
Непересекающиеся множества.

При создании множества ему присваивается уникальный
идентификатор. Поддерживает операции создания множества с определенным
значением, объединения двух множеств и получение значения определенного
множества.
Данные хранятся в дереве. Применяются две оптимизации:

1. Объединение по рангу. Менее глубокое дерево всегда присоединяется к более
глубокому. Таким образом количество операций при поиске корневого множества
сокращается (оно пропорционально глубине дерева).

2. Сжатие путей. При поиске корневого множества каждый узел, не являющийся
корнем, присоединяется к корню. Таким образом сокращается глубина дерева.

Амортизированная сложность всех операций O(log* n), где log* n - итерированный
логарифм, что на практике равно константе.
"""

from typing import Any, Union, Sequence


# noinspection PyShadowingBuiltins
class DisjointSets:

    def __init__(self, accumulate_func) -> None:
        """
        Конструктор.

        :param accumulate_func: функция, задающая что должно быть сделано со
            значениями множеств при слиянии множеств
        """
        # Содержит id родительского множества. Для корней parent[id] == id
        self.parent = []
        # Содержит максимально возможную глубину поддерева
        self.rank = []
        self.values = []
        self.accumulate_func = accumulate_func

    def make_set(self, value: Any) -> int:
        """
        Добавить новое множество с переданным значением.

        :param value: значение, соответствующее множеству
        :return: уникальный идентификатор множества
        """
        self.values.append(value)
        id = len(self.parent)
        self.parent.append(id)
        self.rank.append(0)
        return id

    def find_root_id(self, id: int) -> int:
        """
        Находит id корневого множества для множества с указанным
        идентификатором. Если два множества были объединены когда-либо, то они
        будут иметь одно и то же корневое множество.
        """
        if self.parent[id] != id:
            self.parent[id] = self.find_root_id(self.parent[id])
        return self.parent[id]

    def find_value(self, id: int) -> Any:
        """
        Возвращает значение для множества с переданным идентификатором.
        """
        if id < 0 or id >= len(self.parent):
            raise RuntimeError("No set with id=%d" % id)
        return self.values[self.find_root_id(id)]

    def union(self, id_1: int, id_2: int) -> None:
        """
        Объединить два множества с переданными идентификаторами.
        """
        i_id, j_id = self.find_root_id(id_1), self.find_root_id(id_2)
        if i_id == j_id:
            return
        if self.rank[i_id] > self.rank[j_id]:
            self.parent[j_id] = i_id

            self.values[i_id] = self.accumulate_func(self.values[i_id],
                                                     self.values[j_id])
            self.values[j_id] = None
        elif self.rank[i_id] < self.rank[j_id]:
            self.parent[i_id] = j_id
            self.values[j_id] = self.accumulate_func(self.values[i_id],
                                                     self.values[j_id])
            self.values[i_id] = None
        else:
            self.parent[j_id] = i_id
            self.values[i_id] = self.accumulate_func(self.values[i_id],
                                                     self.values[j_id])
            self.values[j_id] = None
            self.rank[i_id] += 1

    def __len__(self):
        """
        Возвращает общее количество множеств.
        """
        return len(self.parent)


# noinspection PyShadowingBuiltins
class MathDisjointSets(DisjointSets):
    """
    Непересекающееся множество, которое не учитывает значения. Полезно при
    оперировании математическими множествами без акцента на их содержании.
    Соответственно не поддерживает метод find_value(self, id).
    """

    def __init__(self) -> None:
        super().__init__(lambda x, y: None)

    def find_value(self, id: int) -> Any:
        raise NotImplementedError

    def make_set(self, value: Any = None) -> int:
        """
        Добавляет новое множество. Параметр value передавать не нужно.
        """
        return super().make_set(None)


class SumDisjointSets(DisjointSets):
    """
    Непересекающееся множество, которое складывает значения при слиянии
    множеств.
    """

    def __init__(self) -> None:
        super().__init__(lambda x, y: x + y)


class CollectDisjointSets(SumDisjointSets):
    """
    Непересекающееся множество, которое сохраняет значения в списке при слиянии
    множеств.
    """

    def make_set(self, value: Union[Any, Sequence[Any]] = None):
        """
        Создает непересекающееся множество с определенным значением или
        несколькими значениями. Если параметр value отсутствует, то будет
        создано пустое множество.
        """
        if value is None:
            return super().make_set([])
        try:
            return super().make_set([*value])
        except TypeError:
            return super().make_set([value])
