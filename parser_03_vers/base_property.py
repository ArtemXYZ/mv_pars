"""
Парсинг данных с сайта МВидео через API.
"""
# ----------------------------------------------------------------------------------------------------------------------
# import os
# import pandas as pd
# from pandas import DataFrame
import time
# from datetime import datetime
# import json
# import base64
# import urllib.parse
# from bs4 import BeautifulSoup
# from joblib import dump
# from joblib import load
# from tqdm import tqdm
import requests
# import schedule
import random

from parser.params_bank import *  # Все куки хедеры и параметры
from settings.configs import ENGINE

from sqlalchemy.engine import Engine
from requests import Session


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class BaseProperty:
    """Базовый класс для общих атрибутов библиотеки."""

    # Расширения сохраняемых итоговых файлов (не мутабельные):
    __EXTENSION_FILE_DUMP = '.joblib'
    __EXTENSION_FILE_EXCEL = '.xlsx'
    __SESSION: Session = requests.Session()  # Экземпляр сессии:
    # __SCHEDULE = schedule
    def __init__(self):
        # _________________________________________________ Служебные переменные (обеспечивающие сторонние библиотеки)
        # self._SCHEDULE = schedule
        # self.__SESSION: Session = requests.Session()  # Экземпляр сессии:
        self.__CON: Engine = ENGINE
        self.__NAME_TABLE: str = 'current_stock_mvideo'
        self.__SCHEMA: str = 'inlet'
        # _________________________________________________ Входные параметры
        self.__CITY_DATA: list[tuple] = CITY_DATA
        self.__CATEGORY_ID_DATA: tuple = CATEGORY_ID_DATA
        self.__BASE_HEADERS: dict = BASE_HEADERS
        self.__BASE_FOLDER_SAVE: str = '../data/'
        self.__FILE_NAME_BRANCH: str = 'df_branch_data'
        self.__FILE_NAME_CATEGORY: str = 'df_category_data'
        self.__IMITATION_PING_MIN: float | int = 0.5
        self.__IMITATION_PING_MAX: float | int = 2.5
        self.__RETRIES: int = 20  # retries requests
        self.__TIMEOUT: int = 10  # timeout
        # _________________________________________________

    # ------------------------------------------------------------------------------------------------------------------
    # _________________________________________________ VALIDATION
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
    # _________________________________________________
    def _get_retries(self):
        """
        Возвращает заданное количество попыток для повторного подключения, в случае сбоев (обрыв соединения и тд.).
        (геттер).
        """
        return self.__RETRIES

    def _set_retries(self, new_retries_param: int):
        """Передача новых значений количества попыток для повторного подключения, в случае сбоев."""
        self.__RETRIES = self._validation_params(new_retries_param, int, '_set_retries')

    def _get_timeout(self):
        """
        Возвращает заданный промежуток времени между повторными подключениями, в случае сбоев (обрыв соединения и тд.).
        (геттер).
        """
        return self.__TIMEOUT

    def _set_timeout(self, new_timeout_param: int):
        """Передача нового значения промежутка времени между повторными подключениями, в случае сбоев."""
        self.__TIMEOUT = self._validation_params(new_timeout_param, int, '_set_timeout')
    # _________________________________________________
    # _________________________________________________
    def _get_category_id_data(self):
        """Возвращает категории на сайте для поиска подкатегорий парсингом (геттер)."""
        return self.__CATEGORY_ID_DATA

    def _set_category_id_data(self, new_category_data: tuple):
        """Передача новых значений категорий для поиска подкатегорий парсингом."""
        self.__CATEGORY_ID_DATA = self._validation_params(new_category_data, tuple, '_set_category_id_data')
    # _________________________________________________
    # _________________________________________________
    @classmethod
    def _get_session(cls):
        """Возвращает экземпляр сессии (геттер)."""
        return cls.__SESSION

    # Нет сеттора для session!
    # _________________________________________________
    # _________________________________________________
    def _get_connect(self):
        """
        Возвращает экземпляр подключения к базе данных (геттер).
        """
        return self.__CON

    def _set_connect(self, new_connect_obj):
        """
        Передача нового объекта подключения к базе данных.
        """
        self.__CON = self._validation_params(new_connect_obj, Session, '_set_connect')

    # _________________________________________________
    # _________________________________________________
    def _get_name_table(self):
        """
        Возвращает имя таблицы в базе данных определенную по умолчанию для сохранения результатов парсинга (геттер).
        """
        return self.__NAME_TABLE

    def _set_name_table(self, new_name_table):
        """
        Установка нового имени таблицы в базе данных для сохранения результатов парсинга.
        """
        self.__NAME_TABLE = self._validation_params(new_name_table, str, '_set_name_table')
        print(f'Установлено новое значение имени таблицы в базе данных для сохранения результатов парсинга:'
              f' {self.__NAME_TABLE}')

    # _________________________________________________
    # _________________________________________________
    def _get_name_schem(self):
        """
        Возвращает имя схемы, где хранится таблица, определенная по умолчанию для сохранения результатов
        парсинга (геттер).
        """
        return self.__SCHEMA

    def _set_name_schem(self, new_name_schem):
        """Передача нового объекта подключения к базе данных."""
        self.__SCHEMA = self._validation_params(new_name_schem, str, '_set_schem')

    # _________________________________________________
    # _________________________________________________ CITY_DATA
    def _get_city_data(self):
        """
        Возвращает текущие значения переменной CITY_DATA (набор исходных данных, необходимый для работы методов
        парсера (геттер).
        """
        return self.__CITY_DATA

    def _set_city_data(self, new_city_data):
        """
        Обновляет значения по умолчанию переменной CITY_DATA (набор исходных данных, необходимый для работы
        методов парсера (геттер).
        """
        self.__CITY_DATA = self._validation_params(new_city_data, (list, tuple), '_set_city_data')

    # _________________________________________________
    # _________________________________________________ BASE_FOLDER
    def _get_base_folder_save(self):
        """Возвращает текущие значения имени папки для сохранения результатов работы парсера (геттер)."""
        return self.__BASE_FOLDER_SAVE

    def _set_base_folder_save(self, new_folder):
        """Обновляет значения по умолчанию имени папки для сохранения результатов работы парсера (геттер)."""
        self.__BASE_FOLDER_SAVE = self._validation_params(new_folder, str, '_set_base_folder_save')

    # _________________________________________________
    # _________________________________________________ HEADERS
    def _get_headers(self):
        """Возвращает текущие значения заголовков (геттер)."""
        return self.__BASE_HEADERS

    def _set_headers(self, new_headers: dict):
        """Устанавливает новые значения заголовков (cеттер)."""
        self.__BASE_HEADERS = self._validation_params(new_headers, dict, '_set_headers')

    # _________________________________________________
    # _________________________________________________ NAME_BRANCH / NAME_CATEGORY
    def _get_unified_names_files_for_branches(self):
        """Возвращает текущие значения имен итоговых выходных файлов метода получения филиалов (get_shops) (геттер)."""
        return self.__FILE_NAME_BRANCH

    def _set_unified_names_files_for_branches(self, new_name_file: str):
        """Устанавливает новые значения имен итоговых выходных файлов метода получения филиалов (get_shops) (cеттер)."""
        self.__FILE_NAME_BRANCH = self._validation_params(
            new_name_file, str, '_set_unified_names_files_for_branches')

    # __________________________
    def _get_unified_names_files_for_category(self):
        """
        Возвращает текущие значения имен итоговых выходных файлов метода получения категорий (count_product) (геттер).
        """
        return self.__FILE_NAME_CATEGORY

    def _set_unified_names_files_for_category(self, new_name_file: str):
        """
        Устанавливает новые значения имен итоговых выходных файлов метода получения категорий (count_product) (cеттер).
        """
        self.__FILE_NAME_CATEGORY = self._validation_params(
            new_name_file, str, '_set_unified_names_files_for_category')

    # _________________________________________________
    # _________________________________________________ PATH_FILES

    def _get_path_file_branch_dump(self):
        """Формирует путь для сохранения дампа по филиалам."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_branch_excel(self):
        """Формирует путь для сохранения файла excel по филиалам."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_EXCEL}"

    # _________________________________________________
    # _________________________________________________ PATH_FILES

    def _get_path_file_category_dump(self):
        """Формирует путь для сохранения дампа по категориям."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_CATEGORY}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_category_excel(self):
        return f"{self._BASE_FOLDER_SAVE}{self._FILE_NAME_CATEGORY}{self._EXTENSION_FILE_EXCEL}"

    # _________________________________________________
    # _________________________________________________ PINGS
    def _get_ping_limits(self):
        """Возвращает текущие значения имитации задержки (геттер)."""
        return self.__IMITATION_PING_MIN, self.__IMITATION_PING_MAX


    def _set_ping_limits(self, min_ping, max_ping):
        """Устанавливает и проверяет новые значения пределов задержки (cеттер)."""
        if min_ping < 0.5 or max_ping > 60:
            raise ValueError("Минимальное значение должно быть >= 0.5, а максимальное <= 60.")
        if min_ping > max_ping:
            raise ValueError("Минимальное значение не может быть больше максимального.")

        self._IMITATION_PING_MIN = min_ping
        self._IMITATION_PING_MAX = max_ping
        print(f'Установлены новые значения пределов задержки: {min_ping} - {max_ping}')
        # todo:  !! переписать - нужно добавить валидацию.

    def _get_time_sleep_random(self):
        """Случайная задержка для имитации человека во время парсинга."""
        min_ping, max_ping = self._get_ping_limits()
        time.sleep(random.uniform(min_ping, max_ping)) # todo:  !! - return - возможно ошибка.

    # _________________________________________________

# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------
