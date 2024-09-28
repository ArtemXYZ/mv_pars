"""
Универсальные инструменты для парсинга данных через API.
"""
# ----------------------------------------------------------------------------------------------------------------------
import os
import requests
import pandas as pd
from pandas import DataFrame
import time
import schedule
from datetime import datetime
import random
import json
import base64
import urllib.parse
from bs4 import BeautifulSoup
from joblib import dump
from joblib import load
from tqdm import tqdm

from parser.params_bank import *  # Все куки хедеры и параметры
# from settings.configs import engine_mart_sv


# ----------------------------------------------------------------------------------------------------------------------
# raise TypeError(f'Object of type {o.__class__.__name__} '
#                         f'is not JSON serializable')
# ----------------------------------------------------------------------------------------------------------------------

#
# _NAME_TABLE='current_stock_mvideo'
# _SCHEMA='inlet'
# # _CON=engine_mart_sv

#

# _CITY_DATA = CITY_DATA
# _CATEGORY_ID_DATA = CATEGORY_ID_DATA
#

#
# # Переменные для расширений сохраняемых итоговых файлов:
# _EXTENSION_FILE_DUMP = '.joblib'
# _EXTENSION_FILE_EXCEL = '.xlsx'
#
# _FILE_NAME_BRANCH = 'df_branch_data'
# _FILE_NAME_CATEGORY = 'df_category_data'

class ParsAPI:
    """Вспомогательные методы вынесены в отдельный класс."""

    # Создаём сессию:
    _SESSION = requests.Session()
    _IMITATION_PING_MIN = 0.5
    _IMITATION_PING_MAX = 2.5
    _BASE_HEADERS: dict = BASE_HEADERS # В заголовках необходимо указать Юзер Агент для корректных запросов.
    _BASE_FOLDER_SAVE = '../data/'
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        pass
    # ------------------------------------------------------------------------------------------------------------------


    # __________________________________________________________________
    # __________________________________________________________________ BASE_FOLDER
    @classmethod
    def get_base_folder_save(cls):
        """Возвращает текущие значения имени папки для сохранения результатов работы парсера (геттер)."""
        return cls._BASE_FOLDER_SAVE

    @classmethod
    def set_base_folder_save(cls, new_folder):
        """Обновляет значения по умолчанию имени папки для сохранения результатов работы парсера (геттер)."""
        if isinstance(new_folder, str):
            cls._BASE_FOLDER_SAVE = new_folder
            print(f'Новое значение папки для сохранения результатов установлено: {new_folder}')
        else:
            raise ValueError('Неверный тип данных у перданной переменной в "set_base_folder_save". Ожидается строка')
    # __________________________________________________________________
    # __________________________________________________________________ HEADERS
    @classmethod
    def get_headers(cls):
        """Возвращает текущие значения загаловков (геттер)."""
        return cls._BASE_HEADERS

    @classmethod
    def set_headers(cls, headers: dict):
        """Устанавливает новые значения загаловков (cеттер)."""
        if not isinstance(headers, dict):
            raise ValueError("Заголовки должны быть представлены в виде словаря.")
        cls._BASE_HEADERS = headers
    # __________________________________________________________________

    # __________________________________________________________________ PINGS
    @classmethod
    def get_ping_limits(cls):
        """Возвращает текущие значения имитации задержки (геттер)."""
        return cls._IMITATION_PING_MIN, cls._IMITATION_PING_MAX

    @classmethod
    def set_ping_limits(cls, min_ping, max_ping):
        """Устанавливает и проверяет новые значения пределов задержки (cеттер)."""
        if min_ping < 0.5 or max_ping > 60:
            raise ValueError("Минимальное значение должно быть >= 0.5, а максимальное <= 60.")
        if min_ping > max_ping:
            raise ValueError("Минимальное значение не может быть больше максимального.")

        cls._IMITATION_PING_MIN = min_ping
        cls._IMITATION_PING_MAX = max_ping
        print(f'Устанановлены новые значения пределов задержки: {min_ping} - {max_ping}')

    @classmethod
    def _set_time_sleep_random(cls):
        """Случайная задержка для имитации человека во время парсинга."""
        min_ping, max_ping = cls.get_ping_limits()
        time.sleep(random.uniform(min_ping, max_ping))

    # __________________________________________________________________
    # __________________________________________________________________ TOOLS
    @classmethod
    def _check_path_file(cls, path_file):
        """
        Перед сохранением результатов работы парсера проверяем наличие существования директории, если таковой нет,
        то создается.
        """
        # ________________________________________________ CHECK
        # Получаем директорию из пути:
        path_dir = os.path.dirname(path_file)

        # Проверка, существует ли директория, создание её, если нет:
        if not os.path.exists(path_dir):
            os.makedirs(path_dir)


    @classmethod
    def _save_data(cls, df, path_file_dump, path_file_excel):
        """
        Перед сохранением результатов работы парсера проверяем наличие существования директории, если таковой нет,
        то создается.
        """
        # ________________________________________________ CHECK
        cls._check_path_file(path_file_dump)
        cls._check_path_file(path_file_excel)
        # ________________________________________________ SAVE
        # Сохраняем результат парсинга в дамп и в эксель:

        # _name_dump = '../data/df_full_branch_data.joblib'
        dump(df, path_file_dump)

        # _name_excel = '../data/df_full_branch_data.xlsx'
        df.to_excel(path_file_excel, index=False)



    def get_response_master(self,
                            url: str,
                            headers: dict = None,
                            params: dict = None,
                            cookies: dict = None,
                            session=None,
                            json_type=True) -> object:
        """Универсальная функция для запросов с передаваемыми параметрами. Возвращает либо текст либо json (python)."""

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

        return self










    @staticmethod
    def _base64_decoded(url_param_string):
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









    # __________________________________________________________________ encoded
    def url_encoded(self, param_string):
        """Базовый метод кодирования в base64."""
        param_string = str(param_string) # Приводим к str принудительно.
        bytes_string = param_string.encode('utf-8') # Преобразуем строку в байтовый объект (bytes), utf-8:
        base64_encoded = base64.b64encode(bytes_string).decode('utf-8')  # Base64-кодирование
        result_encoded = urllib.parse.quote(base64_encoded)  # URL-кодирование
        return result_encoded
    # __________________________________________________________________
    # __________________________________________________________________ encoded_param_single
    def encoded_param_string(self, key: str, value: str) -> str:
        """Mетод кодирования одиночного параметра (ключ: значение) в base64."""
        value_encoded = self.url_encoded(value)
        return f'&{key}={value_encoded}'

    # def encoded_param_dict(self, key: str, value: str) -> dict:
    #     """Mетод кодирования одиночного параметра (ключ: значение) в base64."""
    #     value_encoded = self.url_encoded(value)
    #     return {key: value_encoded}
    #
    # def encoded_param_tuple(self, key: str, value: str) -> tuple:
    #     """Mетод кодирования одиночного параметра (ключ: значение) в base64."""
    #     value_encoded = self.url_encoded(value)
    #     return (key, value_encoded)
    # __________________________________________________________________
    # __________________________________________________________________ encoded_params_methods
    def encoded_params_list(self, key: str, *values: str) -> list[tuple]:
        """Mетод кодирования параметров в base64 по типу единый ключ: множество значений \
        {ключ 0: значение 0, ключ 0: значение 1, ...}.

        Формирователь параметров: 1.0 если все ключи одинаковые, тогда формируем список картежей.

        Одинаковый ключ: Не все сервисы корректно принимают параметры с одинаковыми ключами. \
        Хотя requests корректно формирует URL с повторяющимися параметрами, сервер может их неправильно обрабатывать.
        filter_params = [
            ('filterParams', results_keys_value[0]),
            ('filterParams', results_keys_value[1]),
        ]
        """
        result_params_list = []
        for value in values:  # Перебираем все значения в *values
            value_encoded = self.url_encoded(value)
            param_string = (key, value_encoded)
            result_params_list.append(param_string)
        return result_params_list

    def encoded_params_monostring(self, key: str, *values: str) -> str:
        """Mетод кодирования параметров в base64 по типу единый ключ: множество значений \
        {ключ 0: значение 0, ключ 0: значение 1, ...}.

        Формирователь параметров: 1 если все ключи одинаковые, тогда формируем строку и встраиваем ее в url.
        """
        temp_params_list  = []
        # Перебираем все значения в *values
        for value in values:
            param_string = f'{key}={self._encoded(value)}'
            temp_params_list.append(param_string)

        result_params = '&'.join(temp_params_list)
        return result_params


# result_params_dict = []
#

    # нужно авторазбиение урл строки и выделение тех частей что будут динамически изменяемы.
    # url_count = f'https://www.mvideo.ru/bff/products/listing?categoryId={category_id}&offset=0&limit=1'


    # Формирователь параметров: 1.0 если все ключи одинаковые, тогда формируем список картежей.
    # Формирователь параметров: 2 если ключи не одинаковые, тогда формируем словарь и пеердаем как параметр.





    @classmethod
    def _count_product_request(cls, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset):

        """
        # ---------------- Расшифрованные filterParams:
        # 1. ["Только в наличии","-9","Да"] = 'WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'
        # 2. ["Забрать из магазина по адресу","-12","S668"] =  \
        WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjY4Il0%3D
        # 3. '["Забрать через 15 минут","-11","S972"]' = \
         WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D

        :param categoryId:
        :type categoryId:
        :return:
        :rtype:
        """

        # Формирование закодированных параметров фильтрации в запросе:
        result_filters_params = cls._encoded_request_input_params(id_branch, region_shop_id)

        # --------------------------------------- Переменные:
        # Базовая строка подключения:
        url_count = f'https://www.mvideo.ru/bff/products/listing?categoryId={category_id}&offset=0&limit=1'
        # categoryId - обязательно

        # Конструктор куков:
        cookies_count_product = {
            'MVID_CITY_ID': city_id,
            'MVID_REGION_ID': region_id,
            'MVID_REGION_SHOP': region_shop_id,
            'MVID_TIMEZONE_OFFSET': timezone_offset,
        }

        # Полная строка с фильтрами:
        full_url = f'{url_count}{result_filters_params}'
        # --------------------------------------- Переменные:

        # ---------------------------------------- Выполняем основной запрос:
        # Запрос на извлечение count_product (на вход бязательны: \
        # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
        data = cls._get_response(url=full_url, headers=cls._BASE_HEADERS, params=None,  # косяк в result_filters_params
                                   cookies=cookies_count_product, session=cls._SESSION)

        return data
    # __________________________________________________________________
    # @classmethod
    # def load_result_pars_in_db(cls, name_path_file_dump):
    #     """
    #     Метод сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга.
    #     """
    #
    #     # ------------------------------------ Загрузка дампа результатов парсинга ------------------------------------
    #     if os.path.isfile(name_path_file_dump):  # Если файл существует,тогда: True
    #         # ------------------------------------
    #         load_damp_df = load(name_path_file_dump)  # Тогда загружаем дамп
    #         print("Дамп успешно загружен!")
    #
    #         current_time  = datetime.now()
    #
    #         # Форматируем время в строку
    #         formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    #         # Добавляем новые колонки со значением 0:
    #         load_damp_df['dt_load'] = formatted_time
    #         # print(load_damp_df)
    #         # ------------------------------------
    #         print("Загрузка DataFrame в базу данных.")
    #         # ------------------------------------
    #         # Загрузка итогового DataFrame в базу данных:
    #         load_damp_df.to_sql(name=cls._NAME_TABLE, schema=cls._SCHEMA, con=cls._CON,
    #                             if_exists='replace', index=False, method='multi')
    #         # Выбираем метод 'replace' для перезаписи таблицы или 'append' для добавления данных
    #         # method='multi' используется для оптимизации вставки большого объема данных.
    #
    #         # Закрытие соединения
    #         cls._CON.dispose()
    #
    #         print("Данные успешно сохранены в базу данных!")
    #
    #     else:
    #         load_damp_df = None
    #         print(f'Отсутствует файл дампа в директории: "{name_path_file_dump}"!')
# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------
# def _get_single_request(self,
    #                         url: str,
    #                         headers: dict = None,
    #                         params: dict = None,
    #                         cookies: dict = None
    #                         ) -> object:
    #     """Функция для одиночных запросов с передаваемыми параметрами."""
    #     # self.cookies = cookies
    #
    #     # Обычный запрос:
    #     response = requests.get(url, headers=headers, params=params, cookies=cookies)
    #
    #     # Выполнение запроса:
    #     if response.status_code == 200:
    #         # Если ответ нужен в html:
    #         data = response.text
    #
    #     else:
    #         data = None
    #         print(f"Ошибка: {response.status_code} - {response.text}")
    #
    #     return data



        # ----------------  Не работает если ожидаем (пердаем) одинаковые ключи ("&filterParams=...24&filterParams=... " )
    # filter_params = {
    #     'filterParams1': results_keys_value[0],
    #     'filterParams2': results_keys_value[1],
    # }

