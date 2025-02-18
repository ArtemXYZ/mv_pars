"""
    pass
"""

import os
import json
import time
import re

import xmltodict
import pandas as pd
from pandas import DataFrame
from joblib import dump
from joblib import load

from parser_04_vers.service_tools import ServiceTools
from parser_04_vers.base_property import BaseProperty
from support_tools.code_printer import *
from support_tools.custom_progress_bar import get_progress

# from apscheduler.schedulers.background import BlockingScheduler
# from apscheduler.triggers.cron import CronTrigger
# ----------------------------------------------------------------------------------------------------------------------
class Branches(ServiceTools):
    """
        Класс отвечает за получение информации по актуальным филиалам М.Видео (парсинг).
    """

    def __init__(self):
        super().__init__()

    def _get_branches_dat(self):
        """
            # Парсинг кодов магазинов и адресов, необходимых для целевого запроса. Необходимо передать куки.
            :param session:
            :type session:
            :param city_data: ['city_name', 'city_id', 'region_id', 'region_shop_id', 'timezone_offset']
            :type city_data: DataFrame
            :param imitation_ping_min: минимальная задержка
            :type imitation_ping_min: float
            :param ping_max: максимальная задержка
            :type ping_max: float
            :return: DataFrame: ['id_branch', 'city_name_branch', , 'address_branch', 'city_id', 'region_id',
            'region_shop_id',
                    'timezone_offse'];
                Если в city_data не найдется исходного города (исходные данные для целевых запросов по городам),
                тогда в  колонки [['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0'
                (останутся с нулевыми (по умолчанию) значениями).

            :rtype:  DataFrame
        """

        # Запрос на коды магазинов и адреса. Необходимо передать куки.
        url_get_branches = "https://www.mvideo.ru/bff/region/getShops"

        # 1. Преобразуем список картежей CITY_DATA в датафрейм:
        df_city_data = pd.DataFrame(self._get_city_data(),
                                    columns=['city_name', 'city_id', 'region_id', 'region_shop_id',
                                             'timezone_offset'])

        # 2. Создаем целевой датафрейм
        df_branch_data = pd.DataFrame(columns=['id_branch', 'city_name_branch', 'address_branch'])

        # Создаем список для добавления отсутствующих городов в CITY_DATA (справочные данные):
        bug_list_city_data = []

        # print(f'==================== Подготовка данных для основного запроса ====================')
        # print(f'Перебираем города присутствия МВидео (датафрейм с исходными справочными данными):')

        # 3. Перебираем построчно датафрейм df_city_data с исходными справочными данными для основного запроса:
        # for index, row in df_city_data.iterrows():
        for index, row in df_city_data.iterrows():

            print(
                BACK_WHITE + BRIGHT_STYLE + LIGHTCYAN + # LIGHTBLACK
                f'============================================================ '
                f'{int(index) + 1}. / {get_progress(index, df_city_data)} % / '
                f'Парсинг данных для города: {row.get('city_name')} '
                f'============================================================'
            )

            time.sleep(0.2)


            city_id = row.get('city_id')
            region_id = row.get('region_id')
            region_shop_id = row.get('region_shop_id')
            time_zone = row.get('timezone_offset')
            city_name_parent = row.get('city_name')

            # 4. Конструктор куков:
            cookies_shops = {'MVID_CITY_ID': city_id, 'MVID_REGION_ID': region_id, 'MVID_REGION_SHOP': region_shop_id,
                             'MVID_TIMEZONE_OFFSET': time_zone}

            # 5. Случайная задержка для имитации человека:
            self._get_time_sleep_random()

            # 6. Выполняем основной запрос на извлечение филиалов в конкретном городе:
            # (на вход обязательны: # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
            data: json = self._get_no_disconnect_request(url=url_get_branches, cookies=cookies_shops)
            # headers=self.__base_headers,  session=self.__session
            # print(f'data = {data}, {cookies_shops}')

            # Если запрос вернул None (по причине ошибок), тогда пропускаем итерацию:
            if data is None:
                continue

            print(f'\n'
                  f'Перебираем все филиалы в теле ответа GET запроса (json) для: {city_name_parent}')

            time.sleep(0.1)
            for numb, shop in enumerate(data['body']['shops']):
                # Можно добавить проверки на пустоту, но пока что не требуется.
                ...

                # Получаем список параметров филиала с использованием get()
                id_branch = shop.get('id', 0)  # Если нет 'id', будет 'ID не указан'
                city_name_branch = shop.get('cityName', 0)  # Если нет 'cityName', будет 'Город не указан'
                address_branch = shop.get('address', 0)  # Если нет 'address', будет 'Адрес не указан'

                print(f'{numb}. id_branch: {id_branch}, city_name_branch: {city_name_branch}, '
                      f'address_branch: {address_branch}')

                # Добавление новой строки в датафрейм: - новое
                df_branch_data.loc[len(df_branch_data.index)] = [id_branch, city_name_branch, address_branch]

                # Завершение прогресс-бара (Перебираем массив JSON)
                # time.sleep(0.1) # - если выставить, то появляется время, но ломается структура принта. !

        # Удаляем дубликаты филиалов ((если хотим забрать товар из города "А", \
        # то на сайте доступны филиалы + из других городов, что порождает дубли, \
        # тк. т.е. же самые города, что есть на выпадающем списке(сайт): "Б", "С", "Д", итд..)
        # так же будут(могут) содержать исходный город "А" если сменить гео локацию на сайте в "Б", "С", "Д" \
        # Итого: цикличность данных.):

        # =============================================================================================
        #       1                   2
        # city_name_branch    city_name_parent      # address

        # г.Бирск             # Бирск               # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо
        # г.Бирск             # Стерлитамак         # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо
        # г.Бирск             # Уфа                 # Бирск, ул. Мира, д.143В, ТК «Семейный», Эльдорадо

        # Удалить дубликаты в DataFrame, оставляя только первые значения - параметр keep='first'
        df_branch_data.drop_duplicates(subset=['id_branch'], keep='first', inplace=True)

        # Добавляем новые колонки со значением 0:
        df_branch_data[['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0'

        # Перебираем по филиалам:
        for index, row in df_branch_data.iterrows():

            city_name = row.get('city_name_branch')

            # Сравниваем города полученные парсингом с городами в исходных данных, при совпадении \
            # подтягиваем недостающие значения (заполняем колонки city_id, region_id, region_shop_id, timezone_offset).
            city_name_branch = city_name[2:]  # г.Самара -> Самара

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

                # print(f'В родительском датафрейме отсутствуют справочные данные для города ({bug_list_city_data})')
                # f'для сопоставления новых найденных филиалов.')

        print(f'В родительском датафрейме отсутствуют справочные данные для города ({bug_list_city_data})')

        df_full_branch_data = df_branch_data

        # # Получаем пути к файлам:
        # dump_path = self._get_path_file_branch_dump()
        # excel_path = self._get_path_file_branch_excel()

        # Сохранение exce/dump:
        # self._save_data(df=df_full_branch_data, path_file_dump=dump_path, path_file_excel=excel_path)
        
        self._save_damp_and_excel(df=df_full_branch_data)

        return df_full_branch_data


class SitemapHandler(ServiceTools):
    """
        Класс содержит методы получения и обработки данных из sitemaps mvideo.
        https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def pars_sitemap_xml(xml_data: bytes):
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

        """

        results = []

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
                # Парсим все айди в урл строке:
                id_list = re.findall(r'\d+', data_row)

                results = results + id_list

        return results

    def _get_categories_id_from_ssitemap(self) -> list:
        """
            Метод получает данные со страницы:

                * https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml
            и обрабатывает все id категорий, содержащихся в url-строке, учитывая сложную логику обработки.
            Для того что бы корректно работать дальше с данными в данном методе на выходе имеются только уникальные id,
            также пропускается одна категория "Установка" - она не дает результатов.
        """

        url_sitemap = 'https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml'

        # Получаем ответ в виде байтов:
        # _xml_byte_data: bytes = self._get_response_json(url_sitemap, mode='bytes')  # text / bytes
        _xml_byte_data: bytes = self._get_no_disconnect_request(url=url_sitemap,  mode='bytes')

        # Получаем все категории (categories_ids) с сайт-мап, [str, ...]:
        _ids = self.pars_sitemap_xml(_xml_byte_data)

        return _ids


class ParsingPattern(Branches, SitemapHandler):
    """
        Конструкции для парсинга на основе ServiceTools методов и других сторонних библиотек.
    """

    def __init__(self):
        super().__init__()


    def _check_load_damp(self, _load_damp):
        """
            Вспаомогательный метод проверки наличия дампа и его загрузки.
            Валидация на верхнем уровне.
        """

        _dump_path = self._get_path_file_branch_dump()
        reason = None


        # Включать только когда необходимо повторно собрать данные.
        if _load_damp is False:

            # 1) Подготовка данных (атрибуты филиалов) для основной функции count_product_request:
            # ----------------------------------------------------------
            df_full_branch_data = self._get_branches_dat()
            if df_full_branch_data is None:
                reason = f'Работа функции "get_shops" завершилась неудачей.'
            # pr.pprint(df_full_branch_data)
            # ----------------------------------------------------------

        # в остальных случаях загружаем дамп данных.
        elif _load_damp is True:

            # _name_dump = '../data/df_full_branch_data.joblib'
            if os.path.isfile(_dump_path):  # Если файл существует, тогда: True

                # _name_dump = '../data/df_full_branch_data.joblib'
                df_full_branch_data = load(_dump_path)  # Тогда загружаем дамп
            else:
                df_full_branch_data = None
                reason = (f'Отсутствует файл дампа в директории: {_dump_path}.\n'
                          f'Запустите функцию повторно, установив параметр "load_damp: bool=False", что бы запустить '
                          f'парсинг о филиалах.\n'
                          f'Это необходимо для выполнения основного запроса к данным о количестве товара по категориям'
                          )

        return df_full_branch_data, reason

    # Основной паттерн содержащий всю логику парсинга (без различных проверочных логик верхнего уровня):
    def _run_pattern_core(self, df):
        """
            ОСновная логика паттерна обработки категорий.

                1. Получаем данные по филиалам;
                2. Получаем список всех* категорий М.Видео;
                3. Обход всех филиалов (на каждый филиал полный цикл обработки категорий):
                    - Получаем генератором (вместо цикла) данные по филиально;
                    - Подставляем данные по филиалу в следующий цикл полной обработки всех категорий для 1-го филдиала.
                4.

                * df == df_full_branch_data (все данные по филиалам, необходимые для последующих запросов).
        """

        # 0) ------------------------------- Объявление глобальных переменных:
        # Итоговый список
        result_data_set: list = []

        # Список ошибок
        bug_list = []

        # Список для отработанных категорий, что бы не повторяться по уже добытым данным.
        # В этот список попадают категории уже извлеченные для итогового дата-сета \
        # (в одном ответе имеется вся структура подкатегорий и главных категорий):
        # P.S. По result_data_set сложнее итерировать (внутри словари, сложнее доставать и сортировать id).
        completed_categories: set = set()  # : list = []

        # 1) ------------------------------- Подготовка данных (очистка):

        # Получаем исходные данные по филиалам (Удаляем строки, где city_id равен 0):
        branch_data_df = df[df['city_id'] != 0]

        # Получаем список всех* категорий с сайта:
        ids: list = self._get_categories_id_from_ssitemap()

        # 2) ------------------------------- Обход всех филиалов:
        """
            Главный цикл (верхнеуровневый). 
            ОСуществляет обход по филиалам (следующая логика будет с айди филиала для одной итеррации этого цикла.)
            (на каждый филиал полный цикл обработки категорий).
        """

        # Итерируем по филиалам:
        for main_index, branch_data_row in branch_data_df.iterrows():

            # Достаем данные из строки датафрейма:
            id_branch = branch_data_row.get('id_branch')
            city_name_branch = branch_data_row.get('city_name_branch')
            city_id = branch_data_row.get('city_id')
            region_id = branch_data_row.get('region_id')
            region_shop_id = branch_data_row.get('region_shop_id')
            timezone_offset = branch_data_row.get('timezone_offset')

            print(
                BACK_WHITE + BRIGHT_STYLE + LIGHTRED + # LIGHTBLACK
                f'============================================================ '
                f'{int(main_index) + 1}. / {get_progress(main_index, branch_data_df)} % / '
                f'Парсинг данных для филиала: {id_branch} '
                f'============================================================'
            )

            time.sleep(0.2)

            # ***

            # 3) ------------------------------- Обход всех категорий:
            """
                Вложенный цикл итераций по всем категориям для одного филиала.
            """

            for sub_index , category_id in enumerate(ids):

                print(
                    BACK_WHITE + BRIGHT_STYLE + LIGHTGREEN +
                    f'============================================================ '
                    f'{int(sub_index) + 1}. / {get_progress(sub_index, ids, 2)} % / '
                    f'Парсинг данных для категории: {category_id} '
                    # f'============================================================'
                )

                time.sleep(0.1)

                # Проверка: отработана ли данная категория уже:
                if category_id in completed_categories:  # completed_categories: set

                    print(
                        f'Пропуск категории id: {category_id}, '
                        f'всего completed_categories: {len(completed_categories)}'
                    )
                    # Если категория уже была обработана, пропускаем ее.
                    continue

                # Случайная задержка для имитации человека:
                self._get_time_sleep_random()

                # 3.1.1.1) Основной запрос (возвращает json (пайтон)):
                json_dict = self._count_product_request(
                    category_id=category_id,
                    id_branch=id_branch,
                    city_id=city_id,
                    region_id=region_id,
                    region_shop_id=region_shop_id,
                    timezone_offset=timezone_offset
                )

                # Обращаемся к нужному контейнеру (отсекаем не нужное):
                # Получаем [{'id': '23715', count': 0, 'name': 'Батуты', 'children': [аналогичная структура], {...}}]
                # categories_data = _json['body']['categories']
                # ------------------------------- alternative
                json_body_data = json_dict.get('body')
                categories_data = json_body_data.get('categories')

                # Извлекаем информацию о главной категории:
                # В структуре ответа будет всегда первым словарем по порядку, несмотря на выбранную категорию:
                # 'categories': [{'id': '31018', ...}].
                # main_id = categories_data[0]['id']
                # ------------------------------- alternative
                if categories_data:

                    first_dict_in_categories_data = categories_data[0]
                    main_id = first_dict_in_categories_data.get('id')

                    # print(f'Начало обработки категории id: {_id}.')
                    # Обходим рекурсивно все вложенные структуры и отдаем список данных. Получаем:
                    # [{'main_id': '31018', 'parent_id': '23715', 'id': '23715', count': 0, 'name': 'Батуты', {...}]
                    self.recursion_by_json(  # result_data_set =
                        branch_id=id_branch,
                        main_id=main_id,
                        parent_id=None,
                        categories_data=categories_data,
                        completed_categories=completed_categories,
                        result_data_set=result_data_set
                    )
                    print(f'Иог обработки категории id: {category_id}:')

                else:
                    # Хранит косяки для всех филиалов в виде кортежа,
                    # где первым идет главная категория, следом дочерняя.
                    # --------------------------- <
                    # P/S: бход будет продолжаться для всех дочерних категорий, т.к. их не будет в ответе
                    # (в ответе содержится вся инфа на текущую, главную и дочерние категории).

                    _bug = main_id, category_id
                    bug_list.append(_bug)  # json_body_data
                    print(f'Добавлено в bug_list: {_bug}')

                # break

            # Очистка:
            completed_categories.clear()
            # bug_list - можно чистить
            print(f'bug_list: {bug_list}')

        return result_data_set
        # ----------------------------------------------------------

    def preparate_results_df(self,result_data_set):
        """
            Метод объединяет логику сохранения данных в дамп, Excel и базы данных.
        """

        # 0. Создание DataFrame из добытых данных:
        result_df = pd.DataFrame(result_data_set)

        # 0.1. Добавляем колонку: дата загрузки (по умолчанию: '_dt_load'):
        self.insert_time_in_df(result_df)

        # Итог result_df: 'branch_id', 'main_id', 'sku_count', 'parent_id', 'category_id',  'category_name', '_dt_load'.

        # 1. Сохраняем результат парсинга в дамп и в эксель:
        self._save_damp_and_excel(df=result_df)  # , path_file_dump=dump_path, path_file_excel=excel_path

        # 2. --------------- Продолжаем обработку напрямую, а не загружая result_df из дампа как в пред. версии.



        # ----------------------------------------- inlet."current_stock_mvideo"
        #                                                      *****
        # 2.1. Подготовка датафрейма для словаря категорий сохраняем в таблицу  inlet."current_stock_mvideo"

        # Вернет копию (inplace=False). Удаляем не нужные категории для данной таблицы
        current_stock_df = result_df.drop(['main_id', 'parent_id', 'category_name'], axis=1, inplace=False)
        # Остаются: 'branch_id', *, 'sku_count', * , 'category_id', '_dt_load'


        # ----------------------------------------- inlet."dictionary_categories_mvideo"
        #                                                      *****
        # 2.2. Подготовка датафрейма для словаря категорий сохраняем в таблицу  inlet."dictionary_categories_mvideo"

        # Вернет копию (inplace=False). Удаляем не нужные категории для данной таблицы
        dictionary_categories_df = result_df.drop(['branch_id', 'sku_count'], axis=1, inplace=False)
        # Остаются: *, 'main_id', * , 'parent_id', 'category_id',  'category_name', '_dt_load'.

        # Переименовние колонки 'category_id'. Перезапишет current_stock_df (inplace=True): будет еще айди записи.
        dictionary_categories_df.rename(columns={'category_id': 'id_category'},  inplace=True)

        # Удаление дубликатов (дистинкт для 'category_name') в DataFrame.
        # Останутся только первые значения - параметр keep='first'
        dictionary_categories_df.drop_duplicates(subset=['category_name'], keep='first', inplace=True)

        # Сброс индекса и переименование его в 'id'
        dictionary_categories_df.reset_index(drop=True, inplace=True)
        dictionary_categories_df.index = dictionary_categories_df.index + 1  # Начинаем с 1 если нужно
        dictionary_categories_df.rename_axis('id', inplace=True)

        return current_stock_df, dictionary_categories_df

    def save_results_in_db(
            self,
            _history,
            _catalog,
            # _load_damp=False,
    ) -> None:  # bool
        """
            Метод для сохранения результатов парсинга в бапзу данных.
        """

        # ---------------------------------  Извлекаем параметры для каждой из таблицы:
        # ---------------- Выбираем конкретные значения (се проверки на нижнем уровне присутствуют):
        schema_history: str = self._get_name_table('history')
        name_table_history: str  = self._get_name_schem('history')
        mode_history: str = self._get_mode_type('history')

        schema_catalog: str = self._get_name_table('catalog')
        name_table_catalog: str  = self._get_name_schem('catalog')
        mode_catalog: str = self._get_mode_type('catalog')

        # --------------------------------- Сохраняем в бд:
        # Загрузка итогового DataFrame в базу данных:

        # Индекс ингнорируется по умолчанию, id генерится на уровне базы данных.
        self.upload_to_db(df=current_stock_df, _schema=schema_history, _name=name_table_history, _mode=mode_history)
        self.upload_to_db(
            df=dictionary_categories_df,
            _schema=schema_catalog,
            _name=name_table_catalog,
            _mode=mode_catalog,
            _index=True  #  Индекс переименован в id.
        )

        # return True

    # +
    def _run_one_cycle_pars(self, load_damp=False):
        """
            Метод запуcка полного цикла парсинга
            (с добычей данных по API с сайта МВидео по филиалам и остатка товара по категориям на них) с сохранением
            результатов в базу данных.

                :param load_damp Режим запуска парсинга филиалов

                :notes: Для парсинга ссылок (айди категорий с сайтмапа) не предусмотрен режим сохранения и загрузки
                в дамп, как для параметра load_damp.

        """
        # ----------------------------------------------------------------------------------
        if not isinstance(load_damp, bool):
            raise ValueError('Параметр "load_damp" должен иметь тип данных bool.')

        # ----------------------------------------------------------------------------------
        # Результат проверки наличия дампа:
        df_full_branch_data, reason = self._check_load_damp(_load_damp=load_damp)

        # Если есть результат загрузки дампа данных по филиалам или парсинга таких данных:
        if df_full_branch_data is not None:

            # Здесь вся основная логика:
            result_data_set = self._run_pattern_core(df=df_full_branch_data)

            # Сервисный метод сохранения полученных данных:
            history_df, catalog_df = self.preparate_results_df(result_data_set)

            # Принимает датафреймы и параметры от верхнего уровня (что бы можно было управлять)
            # todo добавить возможность загрузки спарсенного дампа (обернуть эту ветку в одну функцию).
            self.save_results_in_db(_history=history_df, _catalog=catalog_df)


        # Парсинг остановлен по причине отсутствия файла дампа или подготовка данных в "get_shops" завершилась неудачей:
        else:
            print(f'Запуск парсинга остановлен по причине: {reason}')
            history_df = None

        # Итог код магазина, категория, количество. ['id_branch','name_category','count']
        return history_df, catalog_df

# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------


        # # Создаем целевой итоговый датафрейм, куда будут сохранены данные типа: категория (имя), category_id
        # df_dictionary_categories = pd.DataFrame(
        #     columns=[
        #         'name_category',
        #         'category_id',
        #     ]
        # )

        # # Сброс индекса и переименование его в 'id'
        # df_dictionary_categories.reset_index(drop=True, inplace=True)
        # df_dictionary_categories.index = df_dictionary_categories.index + 1  # Начинаем с 1 если нужно
        # df_dictionary_categories.rename_axis('id', inplace=True)


#     print(
    #         BACK_GREEN + BRIGHT_STYLE +
    #         f'                                                   * Запуск бота *'
    #         f'                                                    ')
    #
    #     print(
    #         BACK_WHITE + BRIGHT_STYLE + LIGHTBLACK +
    #         '==========================================================='
    #         '===========================================================')
    #
    #     print(BLUE + BRIGHT_STYLE + 'Запуск сервисных программ:')
    #     print(GREEN + "< Webhook удален и ожидающие обновления сброшены.")
    #     await startup_service_db()  # session_pool=LOCDB_SESSION
    #     print(BLUE + BRIGHT_STYLE + 'Работа сервисных программ завершена:')
    #     print(BACK_CYAN + LIGHTBLACK + 'Бот запущен, все норм!')
    #             print(BACK_GREEN + RED + BRIGHT_STYLE + 'Бот лег!')





#  # -> yield[tuple[params branch]]
    #         params_branch: Generator[tuple] = self._main_cycle_by_branch(df_branches=branch_data_df)


#         _params_branch = self._sub_cycle_by_branch(
#             category_ids=ids,
#             branch_data_row=params_branch,
#             result_data_set=result_data_set
#         )


#     def _main_cycle_by_branch(self, df_branches) -> Generator[tuple]:
#         """
#             Главный цикл (верхнеуровневый). ОСуществляет обход по филиалам (следующая логика будет с айди филиала для
#             одной итеррации этого цикла.)
#             Возвращает генератор. Нужен что бы разделить вложенные циклы по разные структуры и к тому же для сокращения
#             ресурсозатрат.
#         """
#
#         # Итерируем по филиалам:
#         for index, row in df_branches.iterrows():
#
#             # Достаем данные из строки датафрейма:
#             id_branch = row.get('id_branch')
#             city_name_branch = row.get('city_name_branch')
#             city_id = row.get('city_id')
#             region_id = row.get('region_id')
#             region_shop_id = row.get('region_shop_id')
#             timezone_offset = row.get('timezone_offset')
#
#             print(
#                 BACK_WHITE + BRIGHT_STYLE + LIGHTBLACK +
#                 f'============================================================ '
#                 f'{int(index) + 1}. / {get_progress(index, df_branches)} % / '
#                 f'Парсинг по всем категориям для филиала {id_branch} '
#                 f'============================================================'
#             )
#
#             # Возвращаем данные по одному элементу
#             yield id_branch, city_name_branch, city_id, region_id, region_shop_id, timezone_offset

#     def _sub_cycle_by_branch(
    #             self,
    #             category_ids,
    #             branch_data_row: tuple,
    #             result_data_set: list
    #     ):  #  tuple_itms: Generator[tuple],
    #         """
    #             Цикл итераций по одному филиалу.
    #
    #             # -> yield[tuple[params branch]]
    #             params_branch: Generator[tuple] = self._main_cycle_by_branch(df_branches=branch_data_df)
    #         """
    #
    #         # Список ошибок
    #         bug_list = []
    #
    #         # Список для отработанных категорий, что бы не повторяться по уже добытым данным.
    #         # В этот список попадают категории уже извлеченные для итогового дата-сета \
    #         # (в одном ответе имеется вся структура подкатегорий и главных категорий):
    #         # P.S. По result_data_set сложнее итерировать (внутри словари, сложнее доставать и сортировать id).
    #         completed_categories: set = set()  # : list = []
    #
    #         # Распаковка кортежа параметров для филиала:
    #         id_branch, city_name_branch, city_id, region_id, region_shop_id, timezone_offset = branch_data_row
    #
    #
    #
    #         for category_id in category_ids:
    #
    #
    #             # Проверка: отработана ли данная категория уже:
    #             if category_id in completed_categories:  # completed_categories: set
    #
    #                 print(f'Пропуск категории id: {category_id}, completed_categories: {completed_categories}')
    #                 # Если категория уже была обработана, пропускаем ее.
    #                 continue
    #
    #             # Случайная задержка для имитации человека:
    #             self._get_time_sleep_random()
    #
    #             # 3.1.1.1) Основной запрос (возвращает json (пайтон)):
    #             json_python = self._count_product_request(
    #                 category_id=category_id,
    #                 id_branch=id_branch,
    #                 city_id=city_id,
    #                 region_id=region_id,
    #                 region_shop_id=region_shop_id,
    #                 timezone_offset=timezone_offset
    #             )


# Создаем целевой итоговый датафрейм, куда будут сохранены данные типа: код магазина, категория (имя),
# количество.
# df_fin_category_data = pd.DataFrame(
#     columns=[
#         'id_branch',
#         'main_id',
#         'parent_id'
#         'category_id'
#         'count'
#         'category_name'
#     ]
# )



#     def save_results_in_db(
#             self,
#             _history=current_stock_df,
#             _catalog=dictionary_categories_df,
#             _load_damp=False, _if_exists='append'
#     ) -> bool:
#         """
#             Метод для сохранения результатов парсинга в бапзу данных.
#         """
#
#         # ---------------------------------  Извлекаем параметры для каждой из таблицы:
#         saving_params: dict | None = self.__saving_params_to_dbs.get()
#
#         if not saving_params:
#             raise KeyError(f'Ошибка доступа к параметрам сохранения результатов! Данные отсутствуют: {saving_params}.')
#         # ----------------
#         params_by_history: dict | None = saving_params.get('history')
#         params_by_catalog: dict | None = saving_params.get('catalog')
#
#         if not params_by_history:
#             raise KeyError(
#                 f'Ошибка доступа к параметрам сохранения результатов для таблицы "current_stock", тип "history"! '
#                 f'Данные отсутствуют: {params_by_history}.'
#             )
#
#         if not params_by_catalog:
#             raise KeyError(
#                 f'Ошибка доступа к параметрам сохранения результатов для таблицы "dictionary_categories",'
#                 f' тип "catalog"! Данные отсутствуют: {params_by_catalog}.'
#             )
#
#         # ---------------- Выбираем конкретные значения:
#         schema_history: dict | None = params_by_history.get('schema')
#         name_table_history: dict | None = params_by_history.get('name_table')
#         mode_history: dict | None = params_by_history.get('mode')
#
#         if not schema_history and not name_table_history and not mode_history:
#             raise KeyError(
#                 f'Ошибка извлечения параметров сохранения результатов для таблицы "current_stock", тип "history"! '
#                 f'Данные отсутствуют для одного или нескольких параметров: '
#                 f'"schema_history": {schema_history}, "name_table_history": {name_table_history}, '
#                 f'"mode_history": {mode_history}.'
#             )
#
#         # Сохраняем в бд:
#         # ----------------------------------------------------------