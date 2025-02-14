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
import random   # переопределяется (зацикливание)

from parser_03_vers.params_bank import *  # Все куки хедеры и параметры
from settings.configs import ENGINE

from sqlalchemy.engine import Engine
from requests import Session

# from apscheduler.triggers.cron import CronTrigger
# from apscheduler.schedulers.blocking import BlockingScheduler  # Блокирующий:
# BlockingScheduler блокирует выполнение основного потока программы, пока работает планировщик.
# Это значит, что после вызова scheduler.start(), код ниже не будет выполняться, пока планировщик не завершит
# свою работу (что обычно не происходит в течение обычной работы программы).
# Использование: BlockingScheduler удобно использовать в скриптах, где основная задача — это выполнение запланированных
# задач, и нет необходимости выполнять другие действия в основном потоке. Например, это идеальный выбор для консольных
# приложений, которые должны постоянно работать.

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
        self.__CON: Engine = ENGINE
        self.__NAME_TABLE: str = 'current_stock_mvideo'
        self.__SCHEMA: str = 'inlet'
        # _________________________________________________ Входные параметры
        self.__CITY_DATA: list[tuple] = CITY_DATA
        self.__CATEGORY_ID_DATA: tuple = CATEGORY_ID_DATA
        self.__BASE_HEADERS: dict = BASE_HEADERS
        self.__BASE_FOLDER_SAVE: str = './data/'
        self.__FILE_NAME_BRANCH: str = 'df_branch_data'
        self.__FILE_NAME_CATEGORY: str = 'df_category_data'
        self.__IMITATION_PING_MIN: float | int = 0.5
        self.__IMITATION_PING_MAX: float | int = 2.5
        self.__RETRIES: int = 20  # retries requests
        self.__TIMEOUT: int = 120  # timeout 120
        # _________________________________________________

    # ------------------------------------------------------------------------------------------------------------------
    # _________________________________________________ VALIDATION
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
    # @classmethod
    # def _get_scheduler(cls):
    #     """Возвращает экземпляр scheduler (планировщик) (геттер)."""
    #     return cls.__BLOC_SCHEDULER


    # @classmethod
    # def _get_cron_trigger(cls):
    #     """Возвращает cron_trigger (геттер)."""
    #     return cls.__CRON_TRIGGER

    # def _set_schedule(self, set_func, set_week, set_hour, set_minute):
    #     # def _set_schedule(self, func, cron_string=None):
    #     """
    #     Планировщик запуска задач.
    #     Cron — это система для автоматизации выполнения задач по расписанию в UNIX-подобных операционных системах.
    #     Она использует так называемые cron-выражения для задания времени и частоты выполнения задач.
    #     Классическое cron-выражение состоит из пяти полей, каждое из которых определяет единицу времени:
    #
    #     'cron' - для задания расписания на основе cron-выражений:
    #     (my_function, 'cron', minute=0, hour=12)  # Каждый день в 12:00
    #
    #
    #     'date' - для задания одной задачи на определенную дату и время:
    #     (my_function, 'date', run_date=datetime.now() + timedelta(days=1))  # Через один день
    #
    #      'interval' - для задания задач с регулярным интервалом (например, каждые N минут, секунд и т.д.).
    #     (my_function, 'interval', minutes=10)  # Каждые 10 минут/
    #
    #     :param func: передаваемая функция, метод.
    #     :type func: callable
    #     :param cron_string: крон выражение ('0 12 * * *'  # Каждый день в 12:00).
    #     :type cron_string: str
    #     :return: запуск метода по расписанию.
    #     :rtype: callable
    #     """
    #
    #     func_check = self._validation_params(set_func, callable, '_set_schedule')
    #     day_of_week_check = self._validation_params(set_week, str, '_set_schedule')
    #     hour_check = self._validation_params(set_hour, int, '_set_schedule')
    #     minute_check = self._validation_params(set_minute, int, '_set_schedule')
    #     # print(minute_check)
    #
    #     if func_check and day_of_week_check and hour_check and minute_check:
    #         # cron_trigger = CronTrigger.from_crontab(cron_string)
    #         # self._get_scheduler().add_job(func, trigger=cron_trigger)
    #         self._get_scheduler().add_job(func_check, 'cron',
    #                                       day_of_week=day_of_week_check, hour=hour_check, minute=minute_check)
    #
    #         # self._get_scheduler().start()
    #         # return self
    #         return self._get_scheduler()

    # def _set_schedule_cron(self, func, cron_string):  # cron_string=None
    #     """
    #     Планировщик запуска задач.
    #     Cron — это система для автоматизации выполнения задач по расписанию в UNIX-подобных операционных системах.
    #     Она использует так называемые cron-выражения для задания времени и частоты выполнения задач.
    #     Классическое cron-выражение состоит из пяти полей, каждое из которых определяет единицу времени:
    #
    #     'cron' - для задания расписания на основе cron-выражений:
    #     (my_function, 'cron', minute=0, hour=12)  # Каждый день в 12:00
    #
    #
    #     'date' - для задания одной задачи на определенную дату и время:
    #     (my_function, 'date', run_date=datetime.now() + timedelta(days=1))  # Через один день
    #
    #      'interval' - для задания задач с регулярным интервалом (например, каждые N минут, секунд и т.д.).
    #     (my_function, 'interval', minutes=10)  # Каждые 10 минут/
    #
    #     :param func: передаваемая функция, метод.
    #     :type func: callable
    #     :param cron_string: крон выражение ('0 12 * * *'  # Каждый день в 12:00).
    #     :type cron_string: str
    #     :return: запуск метода по расписанию.
    #     :rtype: callable
    #     """
    #
    #     func_check = self._validation_params(func, callable, '_set_schedule_cron')
    #     cron_string = self._validation_params(cron_string, str, '_set_schedule_cron')
    #
    #     # print(minute_check)
    #
    #     if func_check and cron_string:
    #         cron_trigger = CronTrigger.from_crontab(cron_string)
    #         # print(f'test cron_trigger: {cron_trigger}') ++
    #         scheduler = self._get_scheduler().add_job(func, cron_trigger)
    #         return scheduler  #self._get_scheduler()


    # def _set_cron(self, cron_string):  # cron_string=None  (работает)
    #     """
    #     """
    #     cron_string = self._validation_params(cron_string, str, '_set_cron')
    #
    #     if cron_string:
    #         cron_trigger = CronTrigger()
    #         return cron_trigger.from_crontab(cron_string) # +
    #     else:
    #         raise ValueError(f'Ошибка в "_set_cron": параметры не были переданы (cron_string = {cron_string}).')



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

    def _get_path_file_branch_dump(self) -> str:
        """Формирует путь для сохранения дампа по филиалам."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_branch_excel(self) -> str:
        """Формирует путь для сохранения файла excel по филиалам."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_BRANCH}{self.__EXTENSION_FILE_EXCEL}"

    # _________________________________________________
    # _________________________________________________ PATH_FILES

    def _get_path_file_category_dump(self) -> str:
        """Формирует путь для сохранения дампа по категориям."""
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_CATEGORY}{self.__EXTENSION_FILE_DUMP}"

    def _get_path_file_category_excel(self) -> str:
        return f"{self.__BASE_FOLDER_SAVE}{self.__FILE_NAME_CATEGORY}{self.__EXTENSION_FILE_EXCEL}"

    # _________________________________________________
    # _________________________________________________ PINGS
    def _get_ping_limits(self) -> tuple:
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
        # Здесь произойдет задержка:
        time.sleep(random.uniform(min_ping, max_ping))

    # _________________________________________________

# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------