"""
Хеш-таблицы. Повторяет функциональность встроенного ассоциативного массива.
"""


class ChainHashtable:
    """
    Хеш-таблица с разрешением коллизий методом цепочек. Обеспечивает сложность
    операций О(1+n/m) - по сути константа.
    """

    def __init__(self, initial_capacity=16, load_factor=0.75,
                 multiply_factor=2) -> None:
        super().__init__()
        self.buckets = [[] for _ in range(initial_capacity)]
        self.size = 0
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.multiply_factor = multiply_factor

    def __getitem__(self, item):
        for k, v in self.buckets[hash(item) % self.capacity]:
            if k == item:
                return v
        raise KeyError

    def __setitem__(self, key, value):
        bucket = self.buckets[hash(key) % self.capacity]
        for i in range(len(bucket)):
            k, v = bucket[i]
            if k == key:
                del bucket[i]
                self.size -= 1
                break
        bucket.append((key, value))
        self.size += 1
        if self.size / self.capacity > self.load_factor:
            self._resize()

    def __delitem__(self, key):
        bucket = self.buckets[hash(key) % self.capacity]
        for i in range(len(bucket)):
            k, v = bucket[i]
            if k == key:
                del bucket[i]
                self.size -= 1
                return
        raise KeyError

    def _resize(self):
        old_size = self.capacity
        self.capacity = int(self.capacity * self.multiply_factor)
        self.buckets.extend(([] for _ in range(self.capacity - old_size)))
        for i in range(old_size):
            arr = self.buckets[i][:]
            self.buckets[i] = []
            for k, v in arr:
                bucket = self.buckets[hash(k) % self.capacity]
                bucket.append((k, v))

    def __contains__(self, item):
        for k, v in self.buckets[hash(item) % self.capacity]:
            if k == item:
                return True
        return False

    def __len__(self):
        return self.size


class OpenAddressingHashtable:
    """
    Хеш-таблица с открытой адрессацией.
    """

    DELETED = object()

    def __init__(self, initial_capacity=16, load_factor=0.75,
                 multiply_factor=2) -> None:
        super().__init__()
        self.buckets = [None for _ in range(initial_capacity)]
        self.size = 0
        self.capacity = initial_capacity
        self.load_factor = load_factor
        self.multiply_factor = multiply_factor

    def __getitem__(self, item):
        probe = 0
        while True:
            el = self.buckets[self._hash(item, probe)]
            if el is None:
                raise KeyError
            if el != self.DELETED:
                k, v = el
                if k == item:
                    return v
            if probe == self.capacity:
                self._resize()
                probe = 0
            else:
                probe += 1

    def __setitem__(self, key, value):
        probe = 0
        while True:
            i = self._hash(key, probe)
            el = self.buckets[i]
            if el is None:
                self.buckets[i] = (key, value)
                self.size += 1
                if self.size / self.capacity > self.load_factor:
                    self._resize()
                return
            elif el != self.DELETED and key == el[0]:
                self.buckets[i] = (key, value)
                return
            if probe == self.capacity:
                self._resize()
                probe = 0
            else:
                probe += 1

    def __delitem__(self, key):
        probe = 0
        while True:
            i = self._hash(key, probe)
            el = self.buckets[i]
            if el is None:
                raise KeyError
            if el != self.DELETED and key == el[0]:
                self.buckets[i] = self.DELETED
                self.size -= 1
                break
            if probe == self.capacity:
                self._resize()
                probe = 0
            else:
                probe += 1

    def _hash(self, key, probe):
        return (hash(key) + probe) % self.capacity

    def _resize(self):
        copy = self.buckets[:]
        self.capacity = int(self.capacity * self.multiply_factor)
        self.buckets = [None for _ in range(self.capacity)]
        self.size = 0
        for el in copy:
            if el is not None and el != self.DELETED:
                self[el[0]] = el[1]

    def __contains__(self, item):
        for probe in range(self.capacity):
            i = self._hash(item, probe)
            el = self.buckets[i]
            if el is None:
                return False
            if el != self.DELETED and item == el[0]:
                return True
        return False

    def __len__(self):
        return self.size
