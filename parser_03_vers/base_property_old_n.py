"""
Парсинг данных с сайта МВидео через API.
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
from settings.configs import ENGINE


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class BaseProperty:
    """Базовый класс для общих атрибутов библиотеки."""

    # Расширения сохраняемых итоговых файлов (не мутабельные):
    _EXTENSION_FILE_DUMP = '.joblib'
    _EXTENSION_FILE_EXCEL = '.xlsx'

    def __init__(self):
        # _________________________________________________ Служебные переменные (обеспечивающие сторонние библиотеки)
        self._SCHEDULE = schedule
        self._SESSION = requests.Session()  # Экземпляр сессии:
        self._CON = ENGINE
        self._NAME_TABLE: str = 'current_stock_mvideo'
        self._SCHEMA: str = 'inlet'
        # _________________________________________________ Входные параметры
        self._CITY_DATA: list[tuple] = CITY_DATA
        self._CATEGORY_ID_DATA: tuple = CATEGORY_ID_DATA
        self._BASE_HEADERS: dict = BASE_HEADERS
        self._BASE_FOLDER_SAVE: str = '../data/'
        self._FILE_NAME_BRANCH: str = 'df_branch_data'
        self._FILE_NAME_CATEGORY: str = 'df_category_data'
        self._IMITATION_PING_MIN: float | int = 0.5
        self._IMITATION_PING_MAX: float | int = 2.5

        # _________________________________________________

    # ------------------------------------------------------------------------------------------------------------------
    # _________________________________________________ VALIDATION
    # @classmethod
    # def _get_method_name(cls, method):
    #     """Возвращает имя метода."""
    #     return method.__name__ if method else None

    @classmethod
    def _get_method_name(cls, property_name):
        """Возвращает имя метода-сеттера для заданного свойства."""
        prop = getattr(cls, property_name)
        return prop.fset.__name__ if prop.fset else None

    @staticmethod
    def _validation_params(value: any, check_type: any, fanc_name: str = None) -> object:
        """Валидация параметров метода 'activate'."""
        fanc_name_str = fanc_name if fanc_name else 'значение не передавалось'
        if value:
            if isinstance(value, check_type):
                return value
            else:
                raise TypeError(f'Недопустимый тип данных для аргумента: {value} в методе: {fanc_name_str}.')
        else:
            raise ValueError(
                f'Не был передан обязательный аргумент для одного из параметров в методе: {fanc_name_str}.')

    # _________________________________________________

    #     self._SESSION = requests.Session()  # Экземпляр сессии:
    # self._CON = ENGINE
    # self._NAME_TABLE: str = 'current_stock_mvideo'
    # self._SCHEMA: str = 'inlet'

    # __________________________________________________________________ CITY_DATA
    @property
    def __city_data(self):
        """Возвращает текущие значения переменной CITY_DATA \
        (набор исходных данных, необходимый для работы методов парсера (геттер).
        """
        return self._CITY_DATA

    @__city_data.setter
    def __city_data(self, new_city_data):
        """Обновляет значения по умолчанию переменной CITY_DATA \
        (набор исходных данных, необходимый для работы методов парсера (геттер).
        """
        # if isinstance(new_city_data, dict):
        #     self._CITY_DATA = new_city_data
        # else:
        #     raise ValueError('Неверный тип данных у переданной переменной в "set_city_data". Ожидается словарь')

        self.__city_data = self._validation_params(
            new_city_data,
            (list, tuple),
            self._get_method_name(self.__class__.__city_data.fset)  # Динамически получаем имя сеттера
        )

    # __________________________________________________________________
    # __________________________________________________________________ BASE_FOLDER
    @property
    def base_folder_save(self):
        """Возвращает текущие значения имени папки для сохранения результатов работы парсера (геттер)."""
        return self._BASE_FOLDER_SAVE

    @base_folder_save.setter
    def base_folder_save(self, new_folder):
        """Обновляет значения по умолчанию имени папки для сохранения результатов работы парсера (геттер)."""
        if isinstance(new_folder, str):
            self._BASE_FOLDER_SAVE = new_folder
            print(f'Новое значение папки для сохранения результатов установлено: {new_folder}')
        else:
            raise ValueError('Неверный тип данных у перeданной переменной в "set_base_folder_save". Ожидается строка')

    # __________________________________________________________________

    # __________________________________________________________________ HEADERS
    @property
    def headers(self):
        """Возвращает текущие значения заголовков (геттер)."""
        return self._BASE_HEADERS

    @headers.setter
    def headers(self, headers: dict):
        """Устанавливает новые значения заголовков (cеттер)."""
        if not isinstance(headers, dict):
            raise ValueError("Заголовки должны быть представлены в виде словаря.")
        self._BASE_HEADERS = headers

    # __________________________________________________________________
    # __________________________________________________________________ NAME_BRANCH / NAME_CATEGORY
    @property
    def unified_names_files_for_branches(self):
        """Возвращает текущие значения имен итоговых выходных файлов метода получения филиалов (get_shops) (геттер)."""
        return self._FILE_NAME_BRANCH

    @unified_names_files_for_branches.setter
    def unified_names_files_for_branches(self, name_file: str):
        """Устанавливает новые значения имен итоговых выходных файлов метода получения филиалов (get_shops) (cеттер)."""
        if not isinstance(name_file, str):
            raise ValueError("Новое имя для группы итоговых файлов (get_shops()) должно быть строкой.")
        self._FILE_NAME_BRANCH = name_file

    # __________________________
    @property
    def unified_names_files_for_category(self):
        """
        Возвращает текущие значения имен итоговых выходных файлов метода получения категорий (count_product) (геттер).
        """
        return self._FILE_NAME_CATEGORY

    @unified_names_files_for_category.setter
    def unified_names_files_for_category(self, name_file: str):
        """
        Устанавливает новые значения имен итоговых выходных файлов метода получения категорий (count_product) (cеттер).
        """
        if not isinstance(name_file, str):
            raise ValueError("Новое имя для группы итоговых файлов (get_shops()) должно быть строкой.")
        self._FILE_NAME_CATEGORY = name_file

    # __________________________________________________________________ PATH_FILES

    @property
    def path_file_branch_dump(self):
        """Формирует путь для сохранения дампа по филиалам."""
        return f"{self._BASE_FOLDER_SAVE}{self._FILE_NAME_BRANCH}{self._EXTENSION_FILE_DUMP}"

    @property
    def path_file_branch_excel(self):
        """Формирует путь для сохранения файла excel по филиалам."""
        return f"{self._BASE_FOLDER_SAVE}{self._FILE_NAME_BRANCH}{self._EXTENSION_FILE_EXCEL}"

    # __________________________________________________________________
    # __________________________________________________________________ PATH_FILES
    @property
    def path_file_category_dump(self):
        """Формирует путь для сохранения дампа по категориям."""
        return f"{self._BASE_FOLDER_SAVE}{self._FILE_NAME_CATEGORY}{self._EXTENSION_FILE_DUMP}"

    @property
    def path_file_category_excel(self):
        """Формирует путь для сохранения файла excel по категориям."""
        return f"{self._BASE_FOLDER_SAVE}{self._FILE_NAME_CATEGORY}{self._EXTENSION_FILE_EXCEL}"

    # __________________________________________________________________
    # __________________________________________________________________
    # __________________________________________________________________ PINGS
    @property
    def __ping_limits(self):
        """Возвращает текущие значения имитации задержки (геттер)."""
        return self._IMITATION_PING_MIN, self._IMITATION_PING_MAX

    @__ping_limits.setter
    def __ping_limits(self, min_ping, max_ping):
        """Устанавливает и проверяет новые значения пределов задержки (cеттер)."""
        if min_ping < 0.5 or max_ping > 60:
            raise ValueError("Минимальное значение должно быть >= 0.5, а максимальное <= 60.")
        if min_ping > max_ping:
            raise ValueError("Минимальное значение не может быть больше максимального.")

        self._IMITATION_PING_MIN = min_ping
        self._IMITATION_PING_MAX = max_ping
        print(f'Установлены новые значения пределов задержки: {min_ping} - {max_ping}')

    @property
    def _set_time_sleep_random(self):
        """Случайная задержка для имитации человека во время парсинга."""
        min_ping, max_ping = self.__ping_limits()
        time.sleep(random.uniform(min_ping, max_ping))

    # __________________________________________________________________

# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------
