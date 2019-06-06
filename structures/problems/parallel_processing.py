"""
Задача о параллельной обработке.

По данным n процессорам и m задач надо определить, для каждой из задач, каким
процессором она будет обработана и в какое время. Для каждой задачи передается
длительность ее исполнения.
"""

from typing import Sequence, Tuple, List

from structures.heap import Heap

# Данные по задаче. Задается двумя числами (a, b), где a - номер процессора
# (нумерация с нуля), b - время исполнения (отсчет начинается с нуля)
Metric = Tuple[int, int]


def find_tasks_metrics(n: int, tasks_durations: Sequence[int]) -> List[Metric]:
    """
    Возвращает массив, в котором для каждой задачи указан процессор и время,
    когда задача будет им выполнена.

    :param n: количество процессоров
    :param tasks_durations: массив с длительностями задач
    :return: массив из кортежей (a, b) для каждой задачи, где a - номер
        процессора (нумерация с нуля), b - время исполнения (отсчет начинается
        с нуля)
    """
    # В куче хранятся кортежи - время освобождения процессора и его номер
    p = Heap([(0, proc_num) for proc_num in range(n)])
    res = []
    for i in range(len(tasks_durations)):
        time, p_num = p.extract_min()
        res.append((p_num, time))
        p.insert((time + tasks_durations[i], p_num))
    return res


if __name__ == '__main__':
    assert find_tasks_metrics(2, []) == []
    assert find_tasks_metrics(2, [1]) == [(0, 0)]
    assert find_tasks_metrics(1, [1, 2]) == [(0, 0), (0, 1)]
    assert find_tasks_metrics(2, [1, 2, 3, 4, 5]) == [(0, 0), (1, 0), (0, 1),
                                                      (1, 2), (0, 4)]
    assert find_tasks_metrics(3, [1, 1, 1, 1, 1]) == [(0, 0), (1, 0), (2, 0),
                                                      (0, 1), (1, 1)]
