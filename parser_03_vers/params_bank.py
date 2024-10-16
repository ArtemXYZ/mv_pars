"""Списки данных для различных запросов"""

BASE_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.mvideo.ru/',
    'Origin': 'https://www.mvideo.ru',
}

# https://www.mvideo.ru/bff/region/getShops  +
CITY_DATA: list[tuple] = [
    ('Бузулук', 'CityDE_31010', '4', 'S972', '4'),
    ('Новокуйбышевск', 'CityCZ_3744', '4', 'S972', '4'),
    ('Самара', 'CityCZ_1780', '4', 'S972', '4'),
    ('Бирск', 'CityDE_27142', '10', 'S906', '5'),
    ('Благовещенск', 'CityDE_27146', '10', 'S906', '5'),
    ('Стерлитамак', 'CityR_60', '10', 'S906', '5'),
    ('Уфа', 'CityCZ_2534', '10', 'S906', '5'),
    ('Вольск', 'CityDE_31342', '13', 'S908', '4'),
    ('Маркс', 'CityDE_31350', '13', 'S908', '4'),
    ('Саратов', 'CityCZ_984', '13', 'S908', '4'),
    ('Энгельс', 'CityCZ_2714', '13', 'S908', '4'),
    ('Оренбург', 'CityCZ_6276', '17', 'S930', '5'),
    ('Тольятти', 'CityCZ_6270', '24', 'S924', '4'),
    ('Белорецк', 'CityDE_27134', '27', 'S966', '5'),
    ('Ишимбай', 'CityDE_27162', '58', 'S983', '5'),
    ('Салават', 'CityR_58', '58', 'S983', '5'),
    ('Пенза', 'CityCZ_7182', '59', 'S922', '3'),
    ('Сызрань', 'CityR_109', '75', 'S941', '4'),
    ('Белебей', 'CityDE_27122', '88', 'S984', '5'),
    ('Октябрьский', 'CityCZ_15514', '88', 'S984', '5'),
    ('Туймазы', '24300007', '88', 'S984', '5'),
    ('Новотроицк', 'CityR_70', '99', 'S938', '5'),
    ('Орск', 'CityCZ_15549', '99', 'S938', '5'),
    ('Сыктывкар', 'CityR_102', '102', 'S964', '3'),
    ('Балаково', 'CityR_91', '13', 'S908', '4'),
    ('Сибай', 'CityDE_27110', '27', 'S966', '5'),
    ('Магнитогорск', 'CityR_27', '27', 'S966', '5'),
    ('Чапаевск', 'CityCZ_3798', '4', 'S972', '4'),
]


# Главные категории на сайте (для поиска подкатегорий парсингом):
# CATEGORY_ID_DATA: tuple = (

#     '20', '21', '23', '24', '25',
#     '64', '65', '68', '69', '72', '73', '78', '79', '80', '81', '82', '83',
#     '85', '89', '91', '92', '94', '95', '96', '97', '100',
#     '101', '102', '103', '104', '106',
#     '107', '109', '112', '114', '118', '125', '128', '134', '137', '138', '140', '141', '142',
#     '145', '146', '148', '149', '150', '155', '156', '157', '160', '163', '169', '172', '176',
#     '180', '181', '182', '184', '185', '195', '196', '198', '199', '200', '202', '205', '209',
#     '210', '214', '215', '219', '224', '226', '228', '234', '235', '236', '237', '252', '261',
#     '262', '264', '266', '287', '292', '298', '303', '305', '306', '307', '315', '317', '325',
#     '330', '332', '336', '340', '344', '353', '377', '385', '394', '395', '400', '403',


#      '1462', '1781', '2268', '2288', '2289', '2290', '2337', '2338', '2438', '2445',
#     '2469', '2476', '2478', '2480', '2487', '2547', '2587', '2589', '2590', '2592', '3447', '3627',
#     '3868', '3967', '4027', '4108', '4247', '4331', '4334', '4336', '4338', '4342', '4367',
#     '4892', '4893', '4894', '4895', '4928', '4929', '4930', '4987', '5027', '5247', '5429',
#     '5431', '5432', '5433', '5434', '5435', '5507', '5567', '5587', '5607', '5627', '6367',
#     '6507', '6508', '6527', '6907', '7527', '7628', '7957', '7960', '7967', '8073', '8149',
#     '8173', '8193', '8228', '8287', '8627', '8629', '8696', '8707', '8713', '8969', '9068',
#     '9167', '9231', '9247', '9291', '9378', '9380', '9487', '9492', '22780', '22935', '22987',
#     '23715', '23962', '24244', '24281', '25183', '25312', '25467', '25474', '25498', '25685',
#     '26096', '26137', '26559', '26632', '26709', '26913', '27020', '27212', '30257', '30304',
#     '30370', '30409', '30416', '30421', '30436', '30440', '30445', '30447', '30450', '30452',
#     '30549', '30550', '30551', '30562', '30567', '30568', '30569', '30572', '30573', '30608',
#     '30720', '30843', '31035', '31036', '31037', '31038', '31039', '31040', '31042', '31043',
#     '31045', '31081', '31087', '31089', '31182', '31188', '31265', '31289', '31293', '31343',
#     '31380', '31432', '31520', '31623', '31714', '31716', '31722', '31729', '31731', '31743',
#     '31747', '31772', '32040', '32041', '32042', '32056', '32057', '32058', '32061', '32146',
#     '32157', '32158', '32160', '32161', '32163', '32174', '32329', '32330', '32331', '32332',
#     '32374', '32475', '32483', '32494', '33520', '33521', '33522', '33672', '33698', '33712',
#     '33887', '33910', '33912', '33920', '34065', '34081', '34633', '34716', '34730', '34806',
#     '35216', '35217', '35285', '35286', '35287', '35288', '35289', '35290', '35291',

    # '133', '159',
    # '143', '34111', '34821', '382', '2607', '2207', '342', ('34111', можгут быть дубли выше), '2027',
    # '111', '4947',  '31517', '31518',  '31519', '2687', '110',  '4889', '230', '231',  '31522', '300',
    # '393', '113', '25181', '23498', '27134', '389', '24764', '302', '197', '23229', '4527', '230', '179',
    # '227', '23230', '26714', '383', 5429+ '4109 '7961', '7959', '8655', '8610', '7955',
# )







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
    def convert_value_list_in_int(self, id_data_list: list):
        """
        Создаем новый список со значениями приведенными к int.
        """
        # bags = []
        # int_id_data_list   # else bags.append(search)
        return [search for search in id_data_list if self.validation(search)]

    # 1
    def tuple_to_list(self, in_tuple):  # кортеж в список
        """Преобразование кортежа в список."""
        return list(in_tuple) # data_list

    # 2
    def distinct_value(self, in_list: list):
        """Удаляем дубликаты в списке. Сортируем по возрастапнию"""
        unique_value = list(dict.fromkeys(in_list))  # Словарь автоматически удаляет дубли
        return sorted(unique_value)

    # 3
    def exclude_exceptions(self, in_id_data: list, in_exceptions: list):
        """
        Создаем новый список с учетом исключений
        (игнорируем при генерации нового списка значения из in_exceptions).
        """
        new_id_data = [numb for numb in in_id_data if numb not in in_exceptions]
        return sorted(new_id_data)



    def iter_recurs(self, id_data_list_tmp: list, limit: int, len_id_data: int, gaps: list):

        while len_id_data < limit:

            # Итерируемся по рабочему списку:
            for numb in id_data_list_tmp:
                numb += 1
                if numb not in id_data_list_tmp:  # numb_str != limit and

                    gaps.append(numb)  # Добавляем в список пропусков.
                    print(f'gaps {gaps}')

                    id_data_list_tmp.append(numb)  # Добавляем в проверяемый список.
                    print(f'in_id_data {id_data_list_tmp}')

        # # Итерируемся по рабочему списку:
        # for numb in id_data_list_tmp:
        #
        #      if len_id_data < limit:
        #         numb += 1
        #         if numb not in id_data_list_tmp:  # numb_str != limit and
        #
        #             gaps.append(numb)  # Добавляем в список пропусков.
        #             print(f'gaps {gaps}')
        #
        #             id_data_list_tmp.append(numb)  # Добавляем в проверяемый список.
        #             print(f'in_id_data {id_data_list_tmp}')
        #
        #
        #     # Если достигнут конец массива (не ищем больше пропуски):
        #      elif len_id_data == limit:
        #         print(f'выходим из рекурсии {len_id_data}')
        #         return  # выходим из рекурсии



            # self.core(in_id_data)
        return gaps

    # 4/0
    def core(self, in_id_data: list): # in_numb: int,
        """
        Основная функция,
        генерирует пропущенные значения в масииве, учитывая значения, которые необходимо исключить из поиска.
        """
        # Копируем исходный список в рабочий список:
        id_data_list_tmp = in_id_data.copy()
        print(f'copy {id_data_list_tmp}')

        # Определяем предел итераций:
        limit = max(in_id_data)
        # Определяем длинну массива (списка):
        len_id_data = len(id_data_list_tmp)
        print(f'len_id_data {len_id_data}')

        return self.iter_recurs(id_data_list_tmp=id_data_list_tmp, limit=limit, len_id_data=len_id_data, gaps=self.gaps)

    # 4
    def search_gaps(self, in_id_data: list, in_exceptions: list=None):

        id_data_list = self.tuple_to_list(in_id_data)
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