"""
    Микро модуль для инструмента "Прогресс-бар".
"""


def get_progress(index, array, size_round=0):
    """
        Возвращает % выполнения для имитации "прогресс-бара".

        :param index: Текущий индекс итерации (int).
        :param array: Итерируемый объект (list, DataFrame и т.д.).
        :param size_round: Количество знаков после запятой для округления (int).
        :return: Процент выполнения, округленный до указанного количества знаков.

        строк ({progress:.2f}%)
    """
    progress = ((index + 1) / len(array)) * 100
    return round(progress, size_round)
