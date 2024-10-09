from parser_03_vers.base_property import BaseProperty

import requests
import json
import base64  # переопределяется (зацикливание)
import urllib.parse  # переопределяется (зацикливание)
from datetime import datetime  # переопределяется (зацикливание)
import os
import requests
import pandas as pd
from pandas import DataFrame
import time
# from bs4 import BeautifulSoup
from joblib import dump
from joblib import load
# from apscheduler.triggers.cron import CronTrigger

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class ServiceTools(BaseProperty):
    """Вспомогательные методы вынесены в отдельный класс."""

    def __init__(self):
        super().__init__()  # Наследуем атрибуты из BaseProperty

        self.__session = self._get_session()  # Экземпляр сессии:
        self.__base_headers = self._get_headers()
        self.__name_table = self._get_name_table()
        self.__schema = self._get_name_schem()
        self.__con = self._get_connect()
        # self.__bloc_scheduler = self._get_scheduler()
        # self.__cron_trigger = self._get_cron_trigger


        # pass

    # __________________________________________________________________ TOOLS
    @staticmethod
    def _check_path_file(path_file):
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
            print(f'Создана новая дирректория для сохранения файлов: {path_dir}')

    def _save_data(self, df: DataFrame, path_file_dump, path_file_excel):
        """
        Перед сохранением результатов работы парсера проверяем наличие существования директории, если таковой нет,
        то создаётся.
        """
        # ________________________________________________ CHECK
        self._check_path_file(path_file_dump)
        self._check_path_file(path_file_excel)
        # ________________________________________________ SAVE
        # Сохраняем результат парсинга в дамп и в эксель:
        dump(df, path_file_dump)  # _name_dump = '../data/df_full_branch_data.joblib'
        df.to_excel(path_file_excel, index=False)  # _name_excel = '../data/df_full_branch_data.xlsx'
        print('Результат парсинга успешно сохранен в дамп и в эксель файлы.')

    # def _get_response(self, url: str, params: dict = None, cookies: dict = None, json_type=True) -> object:
    #     """Универсальная функция для запросов с передаваемыми параметрами. """
    #
    #     # Устанавливаем куки в сессии
    #     if self.__session and cookies:
    #         self.__session.cookies.update(cookies)
    #
    #     # Обычный запрос или сессия:
    #     if self.__session:
    #         response = self.__session.get(url, headers=self.__base_headers, params=params)
    #
    #     else:
    #         response = requests.get(url, headers=self.__base_headers, params=params, cookies=cookies)
    #
    #     # Выполнение запроса:
    #     if response.status_code == 200:
    #         if json_type:
    #             data = response.json()  # Если ответ нужен в json:
    #         elif not json_type:
    #             data = response.text  # Если ответ нужен в html:
    #     else:
    #         data = None
    #         print(f"Ошибка: {response.status_code} - {response.text}")
    #     return data

    def _get_response_json(self, url: str = None, params: dict = None, cookies: dict = None) -> object:
        """Функция для запросов с мутабельными параметрами. """

        # Устанавливаем куки в сессии (если были переданы):
        if cookies:
            self.__session.cookies.update(cookies)

        try:
            # Выполнение запроса с сессией
            response = self.__session.get(url=url, headers=self.__base_headers, params=params)
            # Проверка кода ответа
            if response.status_code == 200:
                data = response.json()  # Ответ в формате JSON

            else:
                # Обработка некорректных HTTP ответов
                raise requests.exceptions.HTTPError(f"Ошибка HTTP: {response.status_code} - {response.text}")

        # Перехватываем любые ошибки, включая сетевые и прочие исключения
        except Exception as error_connect:
            raise  # Передача исключения на верхний уровень для обработки
        return data

    def _get_no_disconnect_request(self, url: str = None, params: dict = None, cookies: dict = None):
        # , json_type=True, retries=20, timeout=120
        """
        requests.exceptions.ReadTimeout: если сервер долго не отвечает.
        requests.exceptions.ChunkedEncodingError: разрыв соединения в процессе передачи данных.
        requests.exceptions.RequestException: общее исключение для отлова любых других ошибок,
        связанных с запросами, включая неожиданные сбои.

        Обработка непредвиденных ошибок: Если возникает ошибка, не связанная с потерей соединения или таймаутом,
        она будет обработана блоком except requests.exceptions.RequestException, что предотвратит аварийное
        завершение программы
        """
        attempt = 0  # Количество попыток
        while attempt < self._get_retries():
            try:
                # Основной запрос:
                data = self._get_response_json(url=url, params=params, cookies=cookies)
                return data  # Возвращаем данные, если успешен

            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError) as e:
                # Обработка ошибок соединения
                attempt += 1
                print(
                    f"Ошибка соединения: {e}. Попытка {attempt}/{self._get_retries()}."
                    f" Повтор через {self._get_timeout()} сек.")
                time.sleep(self._get_timeout())  # Тайм-аут перед повторной попыткой

            except requests.exceptions.HTTPError as e:
                # Обработка HTTP ошибок
                print(f"HTTP ошибка: {e}. Попытка {attempt + 1}/{self._get_retries()}.")
                attempt += 1
                time.sleep(self._get_timeout())

            except Exception as e:
                # Обработка любых других ошибок
                print(f"Непредвиденная ошибка: {e}. Прерывание.")
                return None

            print("Не удалось выполнить запрос после нескольких попыток.")
            return None

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

    @staticmethod
    def _encoded_request_input_params(branch_code: str, region_shop_code: str):
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

    def _count_product_request(self, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset):

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
        result_filters_params = self._encoded_request_input_params(id_branch, region_shop_id)

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
        # ---------------------------------------
        # ---------------------------------------- Выполняем основной запрос:
        # Запрос на извлечение count_product (на вход бязательны: \
        # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
        data = self._get_no_disconnect_request(url=full_url, cookies=cookies_count_product)
        return data

    # __________________________________________________________________
    def load_result_pars_in_db(self, name_path_file_dump):
        """
        Метод сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга.
        """
        # ------------------------------------ Загрузка дампа результатов парсинга ------------------------------------
        if os.path.isfile(name_path_file_dump):  # Если файл существует,тогда: True
            # ------------------------------------
            load_damp_df = load(name_path_file_dump)  # Тогда загружаем дамп
            print("Дамп успешно загружен!")

            current_time = datetime.now()

            # Форматируем время в строку
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            # Добавляем новые колонки со значением 0:
            load_damp_df['dt_load'] = formatted_time
            # print(load_damp_df)
            # ------------------------------------
            print("Загрузка DataFrame в базу данных.")
            # ------------------------------------
            # Загрузка итогового DataFrame в базу данных:
            load_damp_df.to_sql(name=self.__name_table, schema=self.__schema, con=self.__con,
                                if_exists='replace', index=False, method='multi')
            # Выбираем метод 'replace' для перезаписи таблицы или 'append' для добавления данных
            # method='multi' используется для оптимизации вставки большого объема данных.

            # Закрытие соединения
            self.__con.dispose()

            print("Данные успешно сохранены в базу данных!")

        else:
            load_damp_df = None
            print(f'Отсутствует файл дампа в директории: "{name_path_file_dump}"!')

    # def _set_schedule(self, func, cron_string=None):
    #     """
    #     Панировщик запуска задач.
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
    #     :param func: пердаваемая функция \ метод.
    #     :type func: object
    #     :param cron_string: крон выражение ('0 12 * * *'  # Каждый день в 12:00).
    #     :type cron_string: str
    #     :return: запуск метода по расписанию.
    #     :rtype: object
    #     """
    #
    #     cron_string_check = self._validation_params(cron_string, str, '_set_schedule')
    #     func_check = self._validation_params(func, callable, '_set_schedule')
    #
    #     if func_check and cron_string_check:
    #         cron_trigger = CronTrigger.from_crontab(cron_string)
    #         self.__bloc_scheduler.add_job(func, trigger=cron_trigger)
    #         self.__bloc_scheduler.start()
    #     # else:
    #     #     raise ValueError(f'Ошибка: {cron_string} не может быть пустым.')


# ----------------------------------------------------------------------------------------------------------------------

