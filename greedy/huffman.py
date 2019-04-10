"""
Кодирование Хаффмана. Надо по строке построить оптимальный беспрефиксный код.
Идея алгоритма состоит в следующем: зная вероятности символов в сообщении, можно
описать процедуру построения кодов переменной длины, состоящих из целого
количества битов. Символам с большей вероятностью ставятся в соответствие более
короткие коды. Коды Хаффмана обладают свойством префиксности (то есть ни одно
кодовое слово не является префиксом другого), что позволяет однозначно их
декодировать.
"""

from collections import Counter
from typing import Dict


class Node:
    """
    Узел в дереве. У каждого узла есть значение - частота. Для листов это
    частота вхождения символа в подстроку, а у прочих узлов - суммарная частота
    потомков. Узел может иметь максимум двух потомков и одного родителя. Также
    узел может иметь код - двоичную запись пути, по которому надо пройти от
    корня дерева до текущего узла. Код левого потомка всегда равен коду родителя
    плюс '0', а правого - плюс '1'.
    """

    parent: 'Node' = None
    l_child: 'Node' = None
    r_child: 'Node' = None
    letter: str = None
    code: str = ''

    def __init__(self, freq: int, letter: str = None) -> None:
        self.freq = freq
        self.letter = letter

    @staticmethod
    def merge(node1: 'Node', node2: 'Node'):
        """
        Создать родительский узел для двух переданных узлов.

        :param node1: узел, который будет левым потомком родительского узла
        :param node2: узел, который будет правым потомком родительского узла
        :return: родительский узел
        """
        res = Node(node1.freq + node2.freq)
        res.add_left_child(node1)
        res.add_right_child(node2)
        return res

    def add_left_child(self, child: 'Node'):
        """ Добавить левого потомка. """
        self.l_child = child
        child.parent = self

    def add_right_child(self, child: 'Node'):
        """ Добавить правого потомка. """
        self.r_child = child
        child.parent = self

    def is_left_child(self):
        """ Проверяет является ли узел левым потомком родительского узла. """
        if self.is_root():
            return False
        return self.parent.l_child == self

    def is_root(self):
        """ Проверяет является ли узел корневым (не имеет родителя). """
        return not self.parent

    def is_leaf(self):
        """ Проверяет является ли узел листом (не имеет потомков). """
        return not self.l_child and not self.r_child


class PriorityQueue(list):
    """
    Простая реализация очереди с приоритетами для узлов дерева. В качестве
    приоритета выступает частота узла. Вставка работает за O(1), а получение
    минимума за O(n).
    """

    def get_min(self) -> Node:
        """ Получить узел с минимальным приоритетом. """
        res = min(self, key=lambda x: x.freq)
        self.remove(res)
        return res


def _build_tree(freq_dict: Dict[str, int]) -> Node:
    """ Строит дерево по словарю из символов с их частотами. """
    queue = PriorityQueue()
    for letter, freq in freq_dict.items():
        queue.append(Node(freq, letter))
    for n in range(len(freq_dict) + 1, 2 * len(freq_dict)):
        node1 = queue.get_min()
        node2 = queue.get_min()
        new_node = Node.merge(node1, node2)
        queue.append(new_node)
    root = queue.get_min()
    # Если у нас строка из одинаковых символов. В этом случае узел этого символа
    # должен быть единственным потомком корневого узла
    if root.is_leaf():
        new_node = Node(root.freq)
        new_node.add_left_child(root)
        return new_node
    else:
        return root


def _fill_encode_dict(root_node: Node, encrypt_dict: Dict[str, str]) -> None:
    """
    Заполняет словарь шифрования кодами символов всех листьев переданного
    дерева.

    :param root_node: корневой узел дерева
    :param encrypt_dict: словарь шифрования
    :return: None
    """
    if not root_node.is_root():
        if root_node.is_left_child():
            root_node.code = root_node.parent.code + '0'
        else:
            root_node.code = root_node.parent.code + '1'
    if root_node.is_leaf():
        encrypt_dict[root_node.letter] = root_node.code
    else:
        if root_node.l_child:
            _fill_encode_dict(root_node.l_child, encrypt_dict)
        if root_node.r_child:
            _fill_encode_dict(root_node.r_child, encrypt_dict)


def get_encrypt_dict(txt: str) -> Dict[str, str]:
    """
    Возвращает словарь с символами из текста и соответствующими им двоичными
    кодами, полученными по алгоритму Хаффмана.
    """
    if not txt:
        return {}
    freq_dict = Counter(txt)
    root = _build_tree(freq_dict)
    encrypt_dict = {}
    _fill_encode_dict(root, encrypt_dict)
    return encrypt_dict


def encrypt(txt: str) -> str:
    """
    Шифрует текст кодом Хаффмана. Сложность алгоритма во многом зависит от
    сложности операций очереди с приоритетами. В данном случае О(n^2).
    """
    encrypt_dict = get_encrypt_dict(txt)
    return ''.join(encrypt_dict[i] for i in txt)


def decrypt(txt: str, encrypt_dict: Dict[str, str]) -> str:
    """
    Дешифрует текст, зашифрованный кодом Хаффмана, по словарю, состоящему из
    букв исходного текста и соответствующих двоичных кодов. Сложность алгоритма
    О(n).
    """
    encrypt_dict = {v: k for k, v in encrypt_dict.items()}
    code, res = '', ''
    for digit in txt:
        code += digit
        if code in encrypt_dict:
            res += encrypt_dict[code]
            code = ''
    return res


if __name__ == '__main__':

    assert get_encrypt_dict('') == {}
    assert get_encrypt_dict('a') == {'a': '0'}
    assert get_encrypt_dict('ab') == {'a': '0', 'b': '1'}
    assert get_encrypt_dict('aa') == {'a': '0'}
    assert get_encrypt_dict('abb') == {'a': '0', 'b': '1'}
    assert get_encrypt_dict('abc') == {'a': '10', 'b': '11', 'c': '0'}
    assert get_encrypt_dict('abacabad') == {'a': '0', 'b': '10',
                                            'c': '110', 'd': '111'}

    assert encrypt('') == ''
    assert encrypt('a') == '0'
    assert encrypt('ab') == '01'
    assert encrypt('aa') == '00'
    assert encrypt('abb') == '011'
    assert encrypt('abc') == '10110'
    assert encrypt('abacabad') == '01001100100111'
    assert len(encrypt('beep boop beer!')) == 40

    texts = ['', 'a', 'ab', 'aa', 'abb', 'abc', 'abacabad', 'beep boop beer!']
    for text in texts:
        assert decrypt(encrypt(text), get_encrypt_dict(text)) == text
