import re
import xmltodict
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
from parser_04_vers.base_property import BaseProperty


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class ServiceTools(BaseProperty):
    """
        Вспомогательные методы вынесены в отдельный класс.
    """

    def __init__(self):
        super().__init__()  # Наследуем атрибуты из BaseProperty

        self.__session = self._get_session()  # Экземпляр сессии:
        self.__base_headers = self._get_headers()
        self.__con = self._get_connect()
        #               ***
        self.__saving_params_to_dbs: dict = self._get_saving_params_to_dbs()

        # self.__name_table = self._get_name_table()
        # self.__schema = self._get_name_schem()
        #               ***

        # self.__bloc_scheduler = self._get_scheduler()
        # self.__cron_trigger = self._get_cron_trigger

    @staticmethod
    def _get_progress(index, array, size_round=0):
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
            print(f'Создана новая директория для сохранения файлов: {path_dir}')

    def _save_damp_and_excel(self, df: DataFrame):  # , path_file_dump, path_file_excel
        """
            Перед сохранением результатов работы парсера проверяем наличие существования директории, если таковой нет,
            то создаётся.
        """

        # 1. Получаем пути к файлам:
        dump_path = self._get_path_file_category_dump()
        excel_path = self._get_path_file_category_excel()

        # print(
        #     f'dump_path: {dump_path}\n'
        #     f'excel_path: {excel_path}'
        # )

        # ________________________________________________ CHECK
        self._check_path_file(dump_path)
        self._check_path_file(excel_path)

        # ________________________________________________ SAVE
        # Сохраняем результат парсинга в дамп и в Excel:
        dump(df, dump_path)  # _name_dump = '../data/df_full_branch_data.joblib'
        df.to_excel(excel_path, index=False)  # _name_excel = '../data/df_full_branch_data.xlsx'

        print('Результат парсинга успешно сохранен в дамп и в Excel файлы.')

    def _get_response_json(
            self, url: str = None, params: dict = None, cookies: dict = None, mode: str = 'json'
    ) -> object | dict | bytes | str:
        """
            Функция для запросов с мутабельными параметрами.

            ! stream=True) - добавить параметр для больших ответов  \
            https://stackoverflow.com/questions/18308529/python-requests-package-handling-xml-response.
        """

        # Устанавливаем куки в сессии (если были переданы):
        if cookies:
            self.__session.cookies.update(cookies)

        try:
            # Выполнение запроса с сессией
            response = self.__session.get(url=url, headers=self.__base_headers, params=params)
            # Проверка кода ответа
            if response.status_code == 200:
                if mode == 'json':
                    data: dict = response.json()  # Ответ в формате JSON
                elif mode == 'text':
                    data: str = response.text
                elif mode == 'bytes':
                    data: bytes = response.content
                else:
                    raise ValueError(f'Ошибка параметра "mode": полученное значение {mode} не валидно.'
                                     f'Допустимый синтаксис: "json" (по умолчанию), "text", "bytes".')
            else:
                # Обработка некорректных HTTP ответов
                raise requests.exceptions.HTTPError(f"Ошибка HTTP: {response.status_code} - {response.text}")

        # Перехватываем любые ошибки, включая сетевые и прочие исключения
        except Exception as error_connect:
            raise  # Передача исключения на верхний уровень для обработки
        return data

    def _get_no_disconnect_request(self, url: str = None, params: dict = None, cookies: dict = None,
                                   mode: str = 'json'):
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

            if attempt > 0:
                print(f"♻️ Повторное соединение, попытка: {attempt} / из {self._get_retries()}.")

            try:
                # Основной запрос:
                data = self._get_response_json(url=url, params=params, cookies=cookies, mode=mode)
                return data  # Возвращаем данные, если успешен

            except (requests.exceptions.ConnectionError,
                    requests.exceptions.Timeout,
                    requests.exceptions.ChunkedEncodingError) as e:
                # Обработка ошибок соединения
                attempt += 1
                print(
                    f"🆘 Ошибка соединения: {e}. Попытка {attempt}/{self._get_retries()}."
                    f"🕑 Повтор через {self._get_timeout()} сек."
                )
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
    def pars_sitemap_xml(xml_data: bytes) -> [str, ...]:
        """
            Вспомогательный метод для обработки данных из xml.

            Внутри используется преобразование xml в словарь с вложенными словарями.
                example = {
                    'urlset':
                        {
                            '@xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                            '@xmlns:news': 'http://www.google.com/schemas/sitemap-news/0.9',
                            '@xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
                            '@xmlns:image': 'http://www.google.com/schemas/sitemap-image/1.1',
                            '@xmlns:video': 'http://www.google.com/schemas/sitemap-video/1.1',

                            'url': [
                                {
                                    'loc': 'https://www.mvideo.ru/sadovaya-tehnika-i-oborudovanie-8027/sadovye-\
                                        telezhki-33570',
                                    'lastmod': '2025-02-07', 'changefreq': 'daily', 'priority': '0.5'
                                },
                                {
                                    'loc': 'https://www.mvideo.ru/sadovaya-tehnika-i-oborudovanie-8027/\
                                        sadovyi-dekor-33716',
                                    'lastmod': '2025-02-07', 'changefreq': 'daily', 'priority': '0.5'
                                },
                            ]
                        }
            Логика: получаем ссылки все с содержанием категорий. Через регулярное выражение отбираем вхождения цифр
            (id категорий), при этом отфильтровываем ссылки с содержанием категорий по установке (они не дают результат,
            мусорные). Далее после получения результатов у нас имеется список с дубликатами категорий, тк в каждой
            ссылке дублируются главная категория и подкатегории. Что бы устранить дубликаты, добавляем этот список
            в сет с результатами, происходит удаление дубликатов.

        """

        results: set = set()
        # Ссылки попавшие под фильтрацию:
        filter_out: set = set()

        # Паттерны регулярных выражений для поиска подстроки в ссылках.

        # Ищет цифры, начинающиеся с дефиса, отбирает только цифры, игнорируя дефис в результате поиска:
        # + проверяет, что за числом следует либо символ /, либо конец строки и игнорирует такие вхождения.
        main_pattern = re.compile(r'(?<!-)-(\d+)(?=/|$)')  # r'\d+'  # r'(?<!-)-\d+' # r'(?<!-)-(\d+)'
        # Ищет вхождения со словом "ustanovka":
        sub_pattern = re.compile(r'\bustanovka\b')

        # Преобразование XML в словарь
        xml_content = xmltodict.parse(xml_data)

        try:
            # Извлекаем основной контейнер с информацией:
            data_list_dict: list[dict, ...] = xml_content['urlset']['url']

        except KeyError as e:
            raise ValueError(
                f'Ошибка извлечения данных при попытке обращении к ключам (dict / list) '
                f'преобразованного xml (Lib: "xmltodict") {e}'
            )

        for data_dict in data_list_dict:

            data_row = data_dict.get('loc')

            if data_row:
                if sub_pattern.search(data_row):
                    filter_out.update(data_row)  # Устарело, заменяем на сеты  append(data_row)
                    # print('Пропуск ссылки с содержанием категории ("ustanovka") ')
                    continue

                # Парсим все айди в урл строке:
                # id_list = re.findall(r'\d+', data_row) # Устарело, замена на более производительное (ниже).
                # Использование re.compile имеет смысл в случаях многократно использования одно и то же рег-выражения:
                id_list: list = main_pattern.findall(data_row)
                # print(id_list)

                # results_temp: set = results_temp + id_list # Устарело, замена на более производительный set.
                results.update(id_list)

        # print(f'Ссылки попавшие под фильтрацию: {filter_out}')

        return list(results)

    def recursion_by_json(
            self,
            branch_id: str | None,
            main_id: str | None,
            parent_id: str | None,
            categories_data: list,
            completed_categories: set,
            result_data_set: list | None = None,
    ) -> None:  # list[dict, ...]
        """
            Метод рекурсивного обхода категорй (необходим для обработки любой глубины вложенностей).

            Обрабатывает структуру:
                [{'id': '23715', count': 0, 'name': 'Батуты', 'children': [аналогичная структура родительской], {...}}]

            :param branch_id:
            :type branch_id:
            :param completed_categories:
            :type completed_categories:
            :param main_id:
            :type main_id:
            :param result_data_set:
            :type result_data_set:
            :param categories_data: Передаем список для наполнения результатов.
            :type categories_data: list | None
            :param parent_id: Родительский айди, передаем в рекурсию тоже.
            :type parent_id: str | None.
            :return:
            :rtype:
        """

        if not isinstance(categories_data, list):
            raise TypeError(f'⛔️ Ошибка, недопустимый тип данных для аргумента "categories_data": '
                            f'{type(categories_data)}. Должен быть "list".')

        if not categories_data:
            raise ValueError(f'⛔️ Ошибка, данные по категориям отсутствуют, значение:  {categories_data}.')

        try:
            # -----------------------------------------
            category_dict: dict = categories_data[0]
            # ***
            category_id: str = category_dict['id']
            sku_count: str = category_dict['count']
            category_name: str = category_dict['name']
            # ***
            children: list = category_dict['children']
            # -----------------------------------------
        except Exception as error:
            raise ValueError(f'⛔️ Ошибка доступа к значениям по индексу при обработке данных по категориям: {error}')

        # Создаем словарь с результатами по категории.
        data_set_row = {
            # *** Доп информацйя для создания карты категорий.
            'branch_id': branch_id,
            'main_id': main_id,
            'parent_id': parent_id,
            # *** Основная информация.
            'category_id': category_id,
            'sku_count': sku_count,
            'category_name': category_name,
        }

        # Сохраняем наработки в общий список:
        result_data_set.append(data_set_row)

        # Добавляем 'id' категории в set отработанных.
        completed_categories.add(category_id)  # set ? set

        print(f'data_set_row: {data_set_row}')

        # Если есть дочерние элементы (подкатегории), то рекурсия:
        # (Если нет дочерних элементов, children == [])
        if children:
            # print(f'Обработка вложенных категорий для main_id: {main_id}, id: {category_id}')
            # Рекурсия:
            self.recursion_by_json(
                branch_id=branch_id,
                main_id=main_id,
                # Если есть наследники передаем id верхнего уровня (по умолчанию None для главных категорий):
                parent_id=category_id,
                categories_data=children,
                completed_categories=completed_categories,
                result_data_set=result_data_set
            )

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

    def _count_product_request(
            self, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset, url=None
    ):

        """
        # ---------------- Расшифрованные filterParams:
        # 1. ["Только в наличии","-9","Да"] = 'WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'
        # 2. ["Забрать из магазина по адресу","-12","S668"] =  \
        WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjY4Il0%3D
        # 3. '["Забрать через 15 минут","-11","S972"]' = \
         WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D

        """

        # Формирование закодированных параметров фильтрации в запросе:
        result_filters_params = self._encoded_request_input_params(id_branch, region_shop_id)

        # --------------------------------------- Переменные:
        # Базовая строка подключения:
        url_count = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0&limit=1'
        # categoryId - обязательно

        # Если необходимо передать url другой:
        if url:
            url_count = url

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
        # Запрос на извлечение count_product (на вход обязательны: \
        # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
        data = self._get_no_disconnect_request(url=full_url, cookies=cookies_count_product)

        return data

    @staticmethod
    def insert_time_in_df(df, name_column: str = '_dt_load') -> None:
        """
            Метод вставляет колонку с датой загрузки (берет текущую дату) в датафрейм.
            ***
            Модифицирует (не возвращает новый датафрейм, а изменяет существующий) переданный датафрейм df in-place,
            добавляя в него новую колонку _dt_load.
        """

        current_time = datetime.now()

        # Форматируем время в строку
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        # Добавляем новые колонки со значением 0:
        df[name_column] = formatted_time

    def upload_to_db(self, df, _name, _schema, _mode, _index=False):
        """
            Загрузка DataFrame в базу данных.
        """

        print(
            f'Начало загрузки DataFrame в базу данных: '
            f'схема "{_schema}", таблица "{_name}", режим сохранения "{_mode}"'
        )

        try:
            df.to_sql(name=_name, schema=_schema, con=self.__con, if_exists=_mode, index=_index, method='multi')

            # Закрытие соединения
            self.__con.dispose()

            print("✅ Данные DataFrame успешно сохранены в базу данных!")

        except Exception as err:
            raise ValueError(
                f'❌ Ошибка сохранения DataFrame в базу данных, параметры: '
                f'схема "{_schema}", таблица "{_name}", режим сохранения "{_mode}".\n'
                f'Подробности: {err}.'
            )

    @staticmethod
    def _load_damp(_dump_path: str) -> DataFrame | None:
        """
            Вспомогательный метод проверки наличия дампа и его загрузки.
            Пример:  _dump_path = '../data/df_full_branch_data.joblib'
        """

        _df = load(_dump_path) if os.path.isfile(_dump_path) else None
        if not _df:
            print(f'❌ Отсутствует файл дампа в директории: {_dump_path}.\n')

        return _df


    # __________________________________________________________________



    # def _set_schedule(self, func, cron_string=None):
    #     """
    #         Панировщик запуска задач.
    #         Cron — это система для автоматизации выполнения задач по расписанию в UNIX-подобных операционных системах.
    #         Она использует так называемые cron-выражения для задания времени и частоты выполнения задач.
    #         Классическое cron-выражение состоит из пяти полей, каждое из которых определяет единицу времени:
    #
    #         'cron' - для задания расписания на основе cron-выражений:
    #         (my_function, 'cron', minute=0, hour=12)  # Каждый день в 12:00
    #
    #
    #         'date' - для задания одной задачи на определенную дату и время:
    #         (my_function, 'date', run_date=datetime.now() + timedelta(days=1))  # Через один день
    #
    #          'interval' - для задания задач с регулярным интервалом (например, каждые N минут, секунд и т.д.).
    #         (my_function, 'interval', minutes=10)  # Каждые 10 минут/
    #
    #         :param func: пердаваемая функция \ метод.
    #         :type func: object
    #         :param cron_string: крон выражение ('0 12 * * *'  # Каждый день в 12:00).
    #         :type cron_string: str
    #         :return: запуск метода по расписанию.
    #         :rtype: object
    #     """
    #
    #     cron_string_check = self._validation_params(cron_string, str, '_set_schedule')
    #     func_check = self._validation_params(func, callable, '_set_schedule')
    #
    #     if func_check and cron_string_check:
    #         cron_trigger = CronTrigger.from_crontab(cron_string)
    #         self.__bloc_scheduler.add_job(func, trigger=cron_trigger)
    #         self.__bloc_scheduler.start()
    # else:
    #     raise ValueError(f'Ошибка: {cron_string} не может быть пустым.')

# ----------------------------------------------------------------------------------------------------------------------
