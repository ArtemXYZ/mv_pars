"""

"""
# ----------------------------------------------------------------------------------------------------------------------
import os
import requests
import pandas as pd
from pandas import DataFrame
import time
from datetime import datetime
import random
import json

import base64
import urllib.parse

from bs4 import BeautifulSoup

from joblib import dump
from joblib import load

# from tqdm import tqdm

from parser.params_bank import *  # Все куки хедеры и параметры
from settings.configs import engine_mart_sv



# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class MvPars:
    """Парсинг количества товаров на остатке по филиалам по расписанию."""

    # Приватные переменные для расширений файлов:
    __EXPANSION_FILE_DUMP = '.joblib'
    __EXPANSION_FILE_EXCEL = '.xlsx'
    # # Создаём сессию:
    # __session = requests.Session()

    # ------------------------------------------------------
    def __init__(self,
                 *,

                 session,
                 # Параметры городов в API МВидео, типа: [('Бузулук',	'CityDE_31010',	'4', 'S972', '4'), ...]:
                 city_data: list[tuple],  # CITY_DATA

                 # В заголовках необходимо указать Юзер Агент для корректных запросов
                 get_headers_base: dict,

                 save_name_dump_branch_data='df_branch_data',
                 save_name_excel_branch_data='df_branch_data',

                 save_name_dump_category_data='df_category_data',
                 save_name_excel_category_data='df_category_data',

                 imitation_ping_min: float = 0.5,
                 imitation_ping_max: float = 1.5,

                 base_folder_save='../data/',
                 ):

        self.session = session
        self.city_data = city_data
        self.get_headers_base = get_headers_base

        # Имена файла для сохранения филиалов:
        self.save_name_dump_branch_data = save_name_dump_branch_data
        self.save_name_excel_branch_data = save_name_excel_branch_data

        # Имена файла для сохранения категорий:
        self.save_name_dump_category_data = save_name_dump_category_data
        self.save_name_excel_category_data = save_name_excel_category_data

        # Пределы рандомной задержки для имитации реального пользователя:
        self.imitation_ping_min = imitation_ping_min
        self.imitation_ping_max = imitation_ping_max

        # Базовая директория для сохранения файлов:
        self.base_folder_save = base_folder_save

    # ------------------------------------------------------
    @classmethod
    def _get_file_name(cls, folder=None, name=None, expansion=None):
        # create_path_name
        return f'{folder}{name}{expansion}'

    # ------------------------------------------------------
    # instance - передаем экземпляр в метод, чтобы использовать его атрибуты.
    @classmethod
    def _get_file_name_branch_dump(cls, instance):
        return MvPars._get_file_name(instance.base_folder_save, instance.save_name_dump_branch_data,
                                     cls.__EXPANSION_FILE_DUMP)

    @classmethod
    def _get_file_name_branch_excel(cls, instance):
        return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_branch_data,
                                  cls.__EXPANSION_FILE_EXCEL)

    @classmethod
    def _get_file_name_category_dump(cls, instance):
        return cls._get_file_name(instance.base_folder_save, instance.save_name_dump_category_data,
                                  cls.__EXPANSION_FILE_DUMP)

    @classmethod
    def _get_file_name_category_excel(cls, instance):
        return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_category_data,
                                  cls.__EXPANSION_FILE_EXCEL)
    # ------------------------------------------------------

    @staticmethod
    def get_response(url: str,
                     headers: dict = None, params: dict = None, cookies: dict = None, session=None,
                     json_type=True) -> object:
        """Универсальная функция для запросов с передаваемыми параметрами. """

        # Устанавливаем куки в сессии
        if session and cookies:
            session.cookies.update(cookies)

        # Обычный запрос или сессия:
        if session:
            response = session.get(url, headers=headers, params=params)

        else:
            response = requests.get(url, headers=headers, params=params, cookies=cookies)

        # Выполнение запроса:
        if response.status_code == 200:

            if json_type:
                # Если ответ нужен в json:
                data = response.json()

            elif not json_type:
                # Если ответ нужен в html:
                data = response.text

        else:
            data = None
            print(f"Ошибка: {response.status_code} - {response.text}")

        return data

    @staticmethod
    def base64_decoded(url_param_string):
        """
        Расшифровка параметров URL.
        :param url_param_string: (base64_string)
        :type url_param_string:
        :return:
        :rtype:
        """

        try:

            # Шаг 1: URL-декодирование
            url_param_string_decoded = urllib.parse.unquote(url_param_string)

            # Шаг 2: Base64-декодирование
            base64_decoded_string = base64.b64decode(url_param_string_decoded).decode('utf-8')

            return base64_decoded_string
        except Exception as e:
            print(f'Ошибка декодирования: {e}')
            return None

    @staticmethod
    def encoded_request_input_params(branch_code: str, region_shop_code: str):

        """
         Формирует закодированные параметры запроса для фильтрации.

        :param branch_code: Код филиала
        :param region_shop_code: Код магазина региона
        :return: Список закодированных параметров фильтра
        :rtype: list

        region_shop_code = 'S906'
        branch_code = 'A311'
        """

        results_keys_value = []

        # 1. Формирование фильтров:
        filter_param_9 = f'["Только в наличии","-9","Да"]'
        filter_param_12 = f'["Забрать из магазина по адресу","-12","{branch_code}"]'
        filter_param_11 = f'["Забрать через 15 минут","-11","{region_shop_code}"]'
        filter_tuple = (filter_param_9, filter_param_12, filter_param_11)

        # 2. Кодирование:
        for param_list in filter_tuple:
            # Преобразование списка в строку
            joined_string = str(param_list)

            encoded_list = joined_string.encode('utf-8')  # Преобразуем списки в строку и кодируем в  в байты 'utf-8':
            base64_encoded = base64.b64encode(encoded_list).decode('utf-8')  # Base64-кодирование
            # print(f"Base64-кодированная строка: {base64_encoded}")
            final_encoded = urllib.parse.quote(base64_encoded)  # URL-кодирование
            # print(f"Итоговый URL-кодированный параметр: {final_encoded}")

            # 3. Сохраняем в виде словаря для передачи как параметр в строку запроса.
            # Добавляем в список результат кодирования:
            results_keys_value.append(final_encoded)  # Ожидаем на выход: [рез1, рез2, рез3]
            # print(results_keys_value)

        filter_params = (f'&filterParams={results_keys_value[0]}'
                         f'&filterParams={results_keys_value[1]}'
                         f'&filterParams={results_keys_value[2]}')

        return filter_params


class BranchesDat(MvPars):
    def get_shops(self):

        # self.CITY_DATA: list[tuple],
        # self.session = MvPars()._session,
        # imitation_ping_min: float = self.imitation_ping_min,

        # imitation_ping_max: float = self.imitation_ping_max,

        # save_name_dump=get_file_name_branch_dump(),
        # save_name_excel=get_file_name_branch_excel()


        """
        # Парсинг кодов магазинов и адресов, необходимых для целевого запроса. Необходимо передать куки.
        :param session:
        :type session:
        :param CITY_DATA: ['city_name', 'city_id', 'region_id', 'region_shop_id', 'timezone_offset']
        :type CITY_DATA: DataFrame
        :param imitation_ping_min: минимальная задержка
        :type imitation_ping_min: float
        :param ping_max: максимальная задержка
        :type ping_max: float
        :return: DataFrame: ['id_branch', 'city_name_branch', , 'address_branch', 'city_id', 'region_id',
         'region_shop_id',
                'timezone_offse'];
            Если в CITY_DATA не найдется исходного города (исходные данные для целевых запросов по городам), тогда в \
            колонки [['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0' (останутся с нулевыми \
            (по умолчанию) значениями).

        :rtype:  DataFrame
        """

        # Запрос на коды магазинов и адреса. Необходимо передать куки.
        self.url_get_shops = "https://www.mvideo.ru/bff/region/getShops"



        # _name_dump = f'../data/{save_name_dump}.joblib'
        # _name_excel = f'../data/{save_name_excel}.xlsx'


        # 1. Преобразуем список картежей CITY_DATA в датафрейм:
        df_city_data = pd.DataFrame(self.city_data,
                                    columns=['city_name', 'city_id', 'region_id', 'region_shop_id',
                                             'timezone_offset'])

        # 2. Создаем целевой датафрейм
        df_branch_data = pd.DataFrame(columns=['id_branch', 'city_name_branch', 'address_branch'])

        # Создаем список для добавления отсутствующих городов в CITY_DATA (справочные данные):
        bug_list_city_data = []

        # print(f'df_city_data {df_city_data}')

        # print(f'==================== Подготовка данных для основного запроса ====================')
        # print(f'Перебираем города присутствия МВидео (датафрейм с исходными справочными данными):')

        # 3. Перебираем построчно датафрейм df_city_data с исходными справочными данными для основного запроса:
        # for index, row in df_city_data.iterrows():
        for index, row in tqdm(df_city_data.iterrows(), ncols=80, ascii=True,
                     desc=f'==================== Обработка данных для следующего города ===================='):
                    # desc = f'================== Подготовка данных для основного запроса =================='):

            # desc - задает статическое описание, которое будет отображаться на протяжении всего выполнения прогресс-бара.
            # параметр total для того, чтобы знать, сколько итераций ему нужно отслеживать.

            city_id = row.get('city_id')
            region_id = row.get('region_id')
            region_shop_id = row.get('region_shop_id')
            time_zone = row.get('timezone_offset')
            city_name_parent = row.get('city_name')


            # 4. Конструктор куков:
            cookies_shops = {'MVID_CITY_ID': city_id, 'MVID_REGION_ID': region_id, 'MVID_REGION_SHOP': region_shop_id,
                             'MVID_TIMEZONE_OFFSET': time_zone}

            # 5. Случайная задержка для имитации человека:
            time.sleep(random.uniform(imitation_ping_min, ping_max))

            # 6. Выполняем основной запрос на извлечение филиалов в конкретном городе:
            # (на вход бязательны: # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
            data: json = MvPars.get_response(url=self.url_get_shops,
                                                     headers=headers_base,
                                                     cookies=cookies_shops,
                                                     session=self._session)
            # print(f'data = {data}, {cookies_shops}')

            # + прогрессбар tqdm
            # 7. Перебираем массив JSON, содержащий информацию о филиалах
            # for shop in tqdm(data['body']['shops'],  ncols=80,  ascii=True,  total=len(data['body']['shops']),
            #                  desc=f'\n'
            #                       f'Перебираем все филиалы в теле ответа GET запроса (json)'):
            print(f'\n'
                  f'Перебираем все филиалы в теле ответа GET запроса (json) для: {city_name_parent}')

            time.sleep(0.1)
            for namb, shop in enumerate(data['body']['shops']):

                # Можно добавить проверки на пустоту, но пока что не требуется.
                ...

                # Получаем список параметров филиала с использованием get()
                id_branch = shop.get('id', 0)  # Если нет 'id', будет 'ID не указан'
                city_name_branch = shop.get('cityName', 0)  # Если нет 'cityName', будет 'Город не указан'
                address_branch = shop.get('address', 0)  # Если нет 'address', будет 'Адрес не указан'

                print(f'{namb}. id_branch: {id_branch}, city_name_branch: {city_name_branch}, '
                      f'address_branch: {address_branch}')


                # Добавление новой строки в датафрейм: - новое
                df_branch_data.loc[len(df_branch_data.index)] = [id_branch, city_name_branch, address_branch]

                # завершение прогресс-бара (Перебираем массив JSON)
                # time.sleep(0.1) # - если выставить, то появляется время, но ломается структура принта. !

        # Удаляем дубликаты илиалов ((если хотим забрать товар из города "А", \
        # то на сайте доступны филиалы + из других городов, что пораждает дубли, \
        # тк. те же самые города что есть на выпадающем списоке(сайт): "Б", "С", "Д", итд..)  \
        # так же  будут(могут) содержать исходный город "А" если сменить геолокацию на сайте в "Б", "С", "Д" \
        # Итого: цикличность данных.):

        # =============================================================================================
        #       1                   2
        # city_name_branch    city_name_parent      # address

        # г.Бирск             # Бирск               # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо
        # г.Бирск             # Стерлитамак         # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо
        # г.Бирск             # Уфа                 # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо

        # Удалить дубликаты в DataFrame, оставляя только первые значения - параметр keep='first'
        df_branch_data.drop_duplicates(subset=['id_branch'],  keep='first', inplace=True)

        # Добавляем новые колонки со значением 0:
        df_branch_data[['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0'

        # Перебираем по филиалам:
        for index, row in df_branch_data.iterrows():

            city_name = row.get('city_name_branch')

            # Сравниваем города полученные парсингом с городами в исходных данных, при совпадении \
            # подтягиваем недостающие значения (заполняем колонки city_id, region_id, region_shop_id, timezone_offset).
            city_name_branch = city_name[2:] # г.Самара -> Самара


            # Ищем в родительском датафрейме значения совпадающие по имени города (оставляем в дф только нужную строку):
            city_row_parent = df_city_data[df_city_data['city_name'] == city_name_branch]

            # Обращаемся к значениям по имени колонки, если DataFrame не пустой:
            if not city_row_parent.empty:
                # Забираем значения, обращаясь к первой строке отфильрованного DataFrame
                city_id = city_row_parent['city_id'].iloc[0]
                region_id = city_row_parent['region_id'].iloc[0]
                region_shop_id = city_row_parent['region_shop_id'].iloc[0]
                time_zone = city_row_parent['timezone_offset'].iloc[0]

                # ---------------
                df_branch_data.loc[index, 'city_id'] = city_id
                df_branch_data.loc[index, 'region_id'] = region_id
                df_branch_data.loc[index, 'region_shop_id'] = region_shop_id
                df_branch_data.loc[index, 'timezone_offset'] = time_zone

            # если в DataFrame city_row_parent=пусто, то ничего не делаем (останутся значения 0, что были по умолчанию \
            # при создании DataFrame).
            else:

                # Проверяем наличие в списке bug_list_city_data такого же города (точное совпадение) с city_name_branch
                for city in bug_list_city_data:

                    if city_name_branch == city:
                        break
                else:
                    # need to add reference cities
                    bug_list_city_data.append(city_name_branch)

                # print(f'В родительском датафрейме тсутствуют справочные данныфе для города ({bug_list_city_data})')
                      # f'для сопоставления новых найденных филиалов.')

        print(f'В родительском датафрейме тсутствуют справочные данныфе для города ({bug_list_city_data})')

        df_full_branch_data = df_branch_data
        # -------------------------------------------------------------------
        # Сохраняем результат парсинга в дамп и в эксель:

        # _name_dump = '../data/df_full_branch_data.joblib'
        save_damp = dump(df_full_branch_data, _name_dump)
        # _name_excel = '../data/df_full_branch_data.xlsx'
        df_full_branch_data.to_excel(_name_excel, index=False)

        return df_full_branch_data





# MvPars.get_response()


# ----------------------------------------------------------------------------------------------------------------------
#     @staticmethod
#     def get_response(self,
#                      url: str, headers: dict = None, params: dict = None, cookies: dict = None, session=None,
#                      json_type=True) -> object:
#         """Универсальная функция для запросов с передаваемыми параметрами. """
#
#         self.url = url
#         self.headers = headers
#         self.params = params
#         self.cookies = cookies
#         self.session = session
#         self.json_type = json_type
#
#         # Устанавливаем куки в сессии
#         if self.session and self.cookies:
#             self.session.cookies.update(self.cookies)
#
#         # Обычный запрос или сессия:
#         if self.session:
#             response = self.session.get(self.url, headers=self.headers, params=self.params)
#
#         else:
#             response = requests.get(self.url, headers=self.headers, params=self.params, cookies=self.cookies)
#
#         # Выполнение запроса:
#         if response.status_code == 200:
#
#             if self.json_type:
#                 # Если ответ нужен в json:
#                 data = response.json()
#
#             elif not self.json_type:
#                 # Если ответ нужен в html:
#                 data = response.text
#
#         else:
#             data = None
#             print(f"Ошибка: {response.status_code} - {response.text}")
#
#         return data


# class Response:
#
#
#     def __init__(self):
#         pass
#
#     def get_response(self,
#                      url: str, headers: dict = None, params: dict = None, cookies: dict = None, session=None,
#                      json_type=True) -> object:
#
#         """Универсальная функция для запросов с передаваемыми параметрами. """
#
#         self.url = url
#         self.headers = headers
#         self.params = params
#         self.cookies = cookies
#         self.session = session
#         self.json_type = json_type
#
#
#         # Устанавливаем куки в сессии
#         if self.session and self.cookies:
#             self.session.cookies.update(cookies)
#
#         # Обычный запрос или сессия:
#         if self.session:
#             response = self.session.get(url, headers=headers, params=params)
#
#         else:
#             response = requests.get(url, headers=headers, params=params, cookies=cookies)
#
#
#         # Выполнение запроса:
#         if response.status_code == 200:
#
#             if self.json_type:
#                 # Если ответ нужен в json:
#                 data = response.json()
#
#             elif not self.json_type:
#                 # Если ответ нужен в html:
#                 data = response.text
#                 # print(f'{data}')
#
#         else:
#             data = None
#             print(f"Ошибка: {response.status_code} - {response.text}")
#
#         return data
# cookies_get_shops: dict,  #=cookies_shops,

# def get_file_name_branch_dump(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_dump_branch_data, self.__EXPANSION_FILE_DUMP)
#
#     def get_file_name_branch_excel(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_excel_branch_data,
#                                     self.__EXPANSION_FILE_EXCEL)
#
#     def get_file_name_category_dump(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_dump_category_data,
#                                     self.__EXPANSION_FILE_DUMP)
#
#     def get_file_name_category_excel(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_excel_category_data,
#                                     self.__EXPANSION_FILE_EXCEL)