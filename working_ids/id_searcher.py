# Эти есть в базе
ID_DATA = (1, 2, 3, 6, 10,)
exceptions = (3,)


class ArraySearcher:

    def __init__(self):
        self.gaps = []  # Пропуски
        # self.id_data_list_tmp = []

    # 0/1
    def validation(self, value: any):
        """Валидация данных. Значения будут приведены к int или возвращены как есть, если это int."""
        if not isinstance(value, (str, int)):
            raise ValueError(f"Неподдерживаемый тип данных: {type(value)} для объекта {value}. "
                             f"Допустимые типы даннных: str, int")

        elif isinstance(value, str):
            try:
                return int(value)
            except ValueError as e:
                print(f"Ошибка: попытка преобразования текста в число. {e}")


        elif isinstance(value, int):
            return value

    # 0/2
    def convert_value_list_in_int(self, id_data_list: list):  # todo: устарело, оставить прозапас.
        """
        Создаем новый список со значениями приведенными к int.
        """
        # bags = []
        # int_id_data_list   # else bags.append(search)
        return [search for search in id_data_list if self.validation(search)]

    # 1
    def tuple_to_list(self, in_tuple):  # кортеж в список  # todo: устарело, оставить прозапас.
        """Преобразование кортежа в список."""
        return list(in_tuple)  # data_list

    # 2
    def distinct_value(self, in_list: list):  # todo: устарело, оставить прозапас. Заменяем сетами: set().
        """Удаляем дубликаты в списке. Сортируем по возрастапнию"""
        unique_value = list(dict.fromkeys(in_list))  # Словарь автоматически удаляет дубли
        return sorted(unique_value)

    # 3
    def exclude_exceptions(self, in_id_data: list,
                           in_exceptions: list):  # todo: устарело, оставить прозапас. Заменяем сетами: set().
        """
        Создаем новый список с учетом исключений
        (игнорируем при генерации нового списка значения из in_exceptions).
        """
        new_id_data = [numb for numb in in_id_data if numb not in in_exceptions]
        return sorted(new_id_data)

    # ------------------------------------------------------------
    def convert_to_set(self, input_data: tuple):
        """
        Создаем set на основе значений tuple, дубликаты удалятся автоматически.
        """
        return set(input_data)

    def iter_recurs(self, id_data_list_tmp: list, limit: int, len_id_data: int, gaps: list):

        # while len_id_data < limit:
        #
        #     # Итерируемся по рабочему списку:
        #     for numb in id_data_list_tmp:
        #         numb += 1
        #         if numb not in id_data_list_tmp:  # numb_str != limit and
        #
        #             gaps.append(numb)  # Добавляем в список пропусков.
        #             print(f'gaps {gaps}')
        #
        #             id_data_list_tmp.append(numb)  # Добавляем в проверяемый список.
        #             print(f'in_id_data {id_data_list_tmp}')

        # # Определяем длинну массива (списка):
        # len_id_data = len(id_data_list_tmp)
        # print(f'len_id_data {len_id_data}')

        # Итерируемся по рабочему списку:
        for numb in id_data_list_tmp:

            if not len_id_data <= limit:
                numb += 1
                if numb not in id_data_list_tmp:  # numb_str != limit and

                    gaps.append(numb)  # Добавляем в список пропусков.
                    print(f'gaps {gaps}')

                    id_data_list_tmp.append(numb)  # Добавляем в проверяемый список.
                    print(f'in_id_data {id_data_list_tmp}')

            # Если достигнут конец массива (не ищем больше пропуски):
            else:
                # elif len_id_data == limit:
                print(f'выходим из рекурсии {len_id_data}')
                return  # выходим из рекурсии

        # self.core(in_id_data)
        return gaps

    # 4/0
    def core(self, in_id_data: list):  # in_numb: int,
        """
        Основная функция,
        генерирует пропущенные значения в масииве, учитывая значения, которые необходимо исключить из поиска.
        """
        # Копируем исходный список в рабочий список:
        id_data_list_tmp = in_id_data.copy()
        print(f'copy {id_data_list_tmp}')

        # Определяем предел итераций:
        limit = max(in_id_data)

        # # Определяем длинну массива (списка):
        # len_id_data = len(id_data_list_tmp)
        # print(f'len_id_data {len_id_data}')

        return self.iter_recurs(id_data_list_tmp=id_data_list_tmp, limit=limit, len_id_data=len_id_data, gaps=self.gaps)

    # 4
    # def search_gaps(self, in_id_data: list, in_exceptions: list=None): ошибочная логика из-за особенностей смещения индексов в списках
    #
    #     id_data_list = self.tuple_to_list(in_id_data)
    #     # print(f'id_data_list {id_data_list}')
    #
    #     int_id_data_list = self.convert_value_list_in_int(id_data_list)
    #     distinct_id_data_list = self.distinct_value(int_id_data_list)
    #     # print(f'distinct_id_data_list {distinct_id_data_list}')
    #
    #     if not in_exceptions is None:
    #         job_list = self.exclude_exceptions(distinct_id_data_list, in_exceptions)
    #         # print(f'job_list {job_list}')
    #     else:
    #         job_list = distinct_id_data_list
    #         # print(f'job_list2 {job_list}')
    #
    #     result_gaps = self.core(job_list)
    #     print(f'Значения, отсутствующие в картеже:\n'
    #           f'{result_gaps}')

    def search_gaps(self, input_id_data: list, input_exceptions: list = None):

        data_set = self.convert_to_set(input_id_data)
        # print(f'id_data_list {id_data_list}')

        int_id_data_list = self.convert_value_list_in_int(id_data_list)
        distinct_id_data_list = self.distinct_value(int_id_data_list)
        # print(f'distinct_id_data_list {distinct_id_data_list}')

        if not in_exceptions is None:
            job_list = self.exclude_exceptions(distinct_id_data_list, in_exceptions)
            # print(f'job_list {job_list}')
        else:
            job_list = distinct_id_data_list
            # print(f'job_list2 {job_list}')

        result_gaps = self.core(job_list)
        print(f'Значения, отсутствующие в картеже:\n'
              f'{result_gaps}')


class Searcher(ArraySearcher):

    def __init(self):
        super().__init()
        self.searcher = ArraySearcher()

    def __str__(self):
        print(f'Класс для работы с пропусками в массивах.')


searcher = ArraySearcher()
searcher.search_gaps(ID_DATA)

# Генерирует пропущенные значения в масииве:
# def search_gaps_numb(ID_DATA: tuple,  exceptions: tuple): # , min=None, max=None
#     "Функция генерирует пропущенные значения в масииве, учитывая значения, которые необходимо исключить из поиска."
#
#     gaps = []
#     for numb in ID_DATA:
#
#         # начала проверяем есть ли это значение в исключениях, пропускаем, если да:
#         if numb in exceptions:
#             pass
#
#         # Ищем, если нет в исключениях:
#         else:
#             # Основная функция:
#             # Если это последнее число в выборке (не ищем больше пропуски):
#             if numb == ID_DATA[-1]:
#                 pass
#
#             else:
#                 next_numb = int(numb) + 1
#                 numb_str = str(next_numb)
#
#                 if numb_str in ID_DATA:
#                     # print(f"Значение {numb_str} есть в кортеже.")
#                     pass
#                 else:
#                     gaps.append(next_numb)
#                     # print(f"Значение {numb_str} отсутствует в кортеже.")
#
#
#     print(f'Значения, отсутствующие в кортеже:\n'
#           f'{gaps}')
#
# # Сравнивает значения 2х массивов:
# def search_gaps_numb_in_array(ID_DATA_1: tuple, ID_DATA_2: tuple):
#
#     pass


# search_gaps_numb(ID_DATA)