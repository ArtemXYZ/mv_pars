"""
Парсинг данных с сайта МВидео через API.
"""
# ----------------------------------------------------------------------------------------------------------------------
# import os
# import pandas as pd
# from pandas import DataFrame
import time

import requests
# import schedule
import random  # переопределяется (зацикливание)

from parser_04_vers.params_bank import *  # Все куки хедеры и параметры
from settings.configs import ENGINE

from sqlalchemy.engine import Engine
from requests import Session


# from apscheduler.schedulers.background import BackgroundScheduler  # Фоновый:
#  BackgroundScheduler работает в фоновом режиме, что позволяет основному потоку продолжать выполнение других задач.
#  Вы можете запускать его в фоновом режиме и выполнять другие операции в основном потоке, пока планировщик работает.
# Использование:
# Это удобный выбор для приложений, где необходимо одновременно выполнять несколько задач, например,
# в веб-приложениях или сервисах, которые должны обрабатывать запросы от пользователей, в то время как запланированные
# задачи продолжают выполняться.


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class BaseProperty:
    """Базовый класс для общих атрибутов библиотеки."""

    # Расширения сохраняемых итоговых файлов (не мутабельные):
    __EXTENSION_FILE_DUMP = '.joblib'
    __EXTENSION_FILE_EXCEL = '.xlsx'
    __SESSION: Session = requests.Session()  # Экземпляр сессии:

    # __BLOC_SCHEDULER = BlockingScheduler()  # __bloc_scheduler
    # __CRON_TRIGGER = CronTrigger  # - не работает

    def __init__(self):
        # _________________________________________________ Служебные переменные (обеспечивающие сторонние библиотеки)
        # self._SCHEDULE = schedule
        # self.__SESSION: Session = requests.Session()  # Экземпляр сессии:
        #               ***
        self.__CON: Engine = ENGINE
        self.__SAVING_PARAMS_TO_DBS: dict = {
            'history': {'schema': 'inlet', 'name_table': 'current_stock_mvideo', 'mode': 'append'},
            'catalog': {'schema': 'inlet', 'name_table': 'dictionary_categories_mvideo', 'mode': 'replace'},
        }
        # _________________________________________________ Входные параметры
        self.__CITY_DATA: list[tuple] = CITY_DATA
        self.__BASE_HEADERS: dict = BASE_HEADERS
        self.__BASE_FOLDER_SAVE: str = './data/'
        self.__FILE_NAME_BRANCH: str = 'df_branch_data'
        self.__FILE_NAME_CATEGORY: str = 'df_category_data'
        self.__IMITATION_PING_MIN: float | int = 0.5
        self.__IMITATION_PING_MAX: float | int = 2.5
        self.__RETRIES: int = 10  # retries requests
        self.__TIMEOUT: int = 120  # timeout 120

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _validation_params(value: any, check_type: any, fanc_name: str = None) -> object:
        """Валидация параметров метода 'activate'."""
        fanc_name_str = fanc_name if fanc_name else 'значение не передавалось'

        # if value:
        #     if isinstance(value, check_type):
        #         return value
        #     else:
        #         raise TypeError(f'Недопустимый тип данных для аргумента: {value} в методе: {fanc_name_str}.')
        # else:
        #     raise ValueError(
        #         f'Не был передан обязательный аргумент для одного из параметров в методе: {fanc_name_str}.')

        if value is not None:  # is not None
            if check_type == callable:  # Проверка, если передан тип callable
                if callable(value):
                    return value
                else:
                    raise TypeError(
                        f'Ожидалась вызываемая функция или метод для аргумента: {value} в методе: {fanc_name_str}.')
            elif isinstance(value, check_type):  # Проверка для других типов
                return value
            else:
                raise TypeError(f'Недопустимый тип данных для аргумента: {value} в методе: {fanc_name_str}.')
        else:
            raise ValueError(
                f'Не был передан обязательный аргумент для одного из параметров в методе: {fanc_name_str}.')

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

    @classmethod
    def _get_session(cls):
        """Возвращает экземпляр сессии (геттер)."""
        return cls.__SESSION

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

    def _get_saving_params_to_dbs(self) -> dict:
        """
            Выдает словарь с параметрами для сохранения результатов парсинга: имени таблицы в базе данных.

            По умолчанию:
                'history': {'schema': 'inlet', 'name_table': 'current_stock_mvideo', 'mode': 'append'},
                'catalog': {'schema': 'inlet', 'name_table': 'dictionary_categories_mvideo', 'mode': 'replace'},
        """
        return self.__SAVING_PARAMS_TO_DBS

    def _set_saving_params_to_dbs(self, new_saving_params: dict) -> None:
        """
            Переопределяем...
            :param new_saving_params:
            :type new_saving_params:
            :return:
            :rtype:
        """

        new_params = self._validation_params(new_saving_params, dict, '_set_saving_params_to_dbs')

        if not new_params:
            raise KeyError(
                f'Ошибка обновления параметров сохранения результатов для таблиц! '
                f'Переданный аргумент не должен быть пустым {new_params}.'
            )

        self.__SAVING_PARAMS_TO_DBS = new_params
        print(
            f'Установлено новое значение параметров сохранения результатов парсинга в базе данных:'
            f' {self.__SAVING_PARAMS_TO_DBS}'
        )

    def _get_name_table(self, params_for_table_tag: str) -> str:
        """
            Возвращает имя таблицы в базе данных определенную по умолчанию для сохранения результатов парсинга.
            :param: params_for_table_tag ('history' or 'catalog').
        """

        table_tag = self._validation_params(params_for_table_tag, str, '_get_name_table')
        tag_data: dict = self.__SAVING_PARAMS_TO_DBS.get(table_tag)  # 'history' or 'catalog'

        if tag_data:

            name_table: str = tag_data.get('name_table')

            if not name_table:
                raise KeyError(
                    f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                    f'Отсутствуют данные для имени таблицы: {name_table}.'
                )
        else:
            raise KeyError(
                f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                f'Данные отсутствуют: {tag_data}.'
            )

        return name_table

    def _set_name_table(self, new_name_table, params_for_table_tag):
        """
            Установка нового имени таблицы базы данных для сохранения результатов парсинга.
            :param: params_for_table_tag ('history' or 'catalog').
            :param: new_name_table.
        """

        new_name_table = self._validation_params(new_name_table, str, '_set_name_table')
        table_tag = self._validation_params(params_for_table_tag, str, '_set_name_table')
        tag_data: dict = self.__SAVING_PARAMS_TO_DBS.get(table_tag)  # 'history' or 'catalog'
        tag_data['name_table'] = new_name_table

        print(f'Установлено новое значение имени таблицы в базе данных для сохранения результатов парсинга:'
              f' {tag_data['name_table']}')

    def _get_name_schem(self, params_for_table_tag: str) -> str:
        """
            Возвращает имя схемы, где хранится таблица, определенная по умолчанию для сохранения результатов
            парсинга.
        """

        schem_tag = self._validation_params(params_for_table_tag, str, '_get_name_schem')
        tag_data: dict = self.__SAVING_PARAMS_TO_DBS.get(schem_tag)  # 'history' or 'catalog'

        if tag_data:

            schema_table: str = tag_data.get('schema')

            if not schema_table:
                raise KeyError(
                    f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                    f'Отсутствуют данные для мени схемы: {schema_table}.'
                )
        else:
            raise KeyError(
                f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                f'Данные отсутствуют: {tag_data}.'
            )

        return schema_table

    # def _set_name_schem(self, new_name_schem):
    #     """Передача нового объекта подключения к базе данных."""
    #     self.__SCHEMA = self._validation_params(new_name_schem, str, '_set_schem')

    def _get_mode_type(self, params_for_table_tag: str) -> str:
        """
            Возвращает имя схемы, где хранится таблица, определенная по умолчанию для сохранения результатов
            парсинга (геттер).
        """

        mode_tag = self._validation_params(params_for_table_tag, str, '_get_mode_type')
        tag_data: dict = self.__SAVING_PARAMS_TO_DBS.get(mode_tag)  # 'history' or 'catalog'

        if tag_data:

            mode: str = tag_data.get('mode')

            if not mode:
                raise KeyError(
                    f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                    f'Отсутствуют данные для типа режима сохранения: {mode}.'
                )
        else:
            raise KeyError(
                f'Ошибка доступа к параметрам сохранения результатов для таблицы типа "{params_for_table_tag}"! '
                f'Данные отсутствуют: {tag_data}.'
            )

        return mode

    #  Сетеер

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

    def _get_base_folder_save(self):
        """
            Возвращает текущие значения имени папки для сохранения результатов работы парсера (геттер).
        """
        return self.__BASE_FOLDER_SAVE

    def _set_base_folder_save(self, new_folder):
        """Обновляет значения по умолчанию имени папки для сохранения результатов работы парсера (геттер)."""
        self.__BASE_FOLDER_SAVE = self._validation_params(new_folder, str, '_set_base_folder_save')

    def _get_headers(self):
        """
            Возвращает текущие значения заголовков (геттер).
        """
        return self.__BASE_HEADERS

    def _set_headers(self, new_headers: dict):
        """Устанавливает новые значения заголовков (cеттер)."""
        self.__BASE_HEADERS = self._validation_params(new_headers, dict, '_set_headers')

    def _get_unified_names_files_for_branches(self):
        """
            Возвращает текущие значения имен итоговых выходных файлов метода получения филиалов (get_shops).
        """
        return self.__FILE_NAME_BRANCH

    def _set_unified_names_files_for_branches(self, new_name_file: str):
        """Устанавливает новые значения имен итоговых выходных файлов метода получения филиалов (get_shops) (cеттер)."""
        self.__FILE_NAME_BRANCH = self._validation_params(
            new_name_file, str, '_set_unified_names_files_for_branches')

    def _get_unified_names_files_for_category(self):
        """
            Возвращает текущие значения имен итоговых выходных файлов метода получения категорий.
        """
        return self.__FILE_NAME_CATEGORY

    def _set_unified_names_files_for_category(self, new_name_file: str):
        """
            Устанавливает новые значения имен итоговых выходных файлов метода получения категорий (count_product)
            (cеттер).
        """
        self.__FILE_NAME_CATEGORY = self._validation_params(
            new_name_file, str, '_set_unified_names_files_for_category')

    def _get_path_file_branch_dump(self):
        """
            Формирует путь для сохранения дампа данных по филиалам.
        """
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_branch_excel(self):
        """
            Формирует путь для сохранения файла excel по филиалам.
            """
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_EXCEL}"

    def _get_path_file_category_dump(self):
        """
            Формирует путь для сохранения дампа данных по категориям.
        """
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_CATEGORY}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_category_excel(self):
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_CATEGORY}{self.__EXTENSION_FILE_EXCEL}"

    def _get_ping_limits(self):
        """
            Возвращает текущие значения имитации задержки (минимальные и максимальные границы).
        """
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
        """
            Случайная задержка для имитации человека во время парсинга. Возвращает саму задержку.
        """
        min_ping, max_ping = self._get_ping_limits()
        time.sleep(random.uniform(min_ping, max_ping))

# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------
