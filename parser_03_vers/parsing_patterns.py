from parser_03_vers.service_tools import ServiceTools
from parser_03_vers.base_property import BaseProperty

import os
import pandas as pd
from pandas import DataFrame
from tqdm import tqdm
import json
import time
from joblib import dump
from joblib import load

from apscheduler.schedulers.background import BlockingScheduler
# ----------------------------------------------------------------------------------------------------------------------
class ParsingPatterns(ServiceTools, BaseProperty):
    """Частные конструкции для парсинга на основе ServiceTools методов и других сторонних библиотек."""

    def __init__(self):
        super().__init__()  # Наследуем атрибуты из ServiceTools
        # self.__city_data = self._get_city_data()
        # self.__category_id_data = self._get_category_id_data()
        # self.__base_headers = self._get_headers()
        # self.__session = self._get_session()
        # pass
    # ------------------------------------------------------------------------------------------------------------------
    # __________________________________________________________________ GET_SHOPS
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
            Если в city_data не найдется исходного города (исходные данные для целевых запросов по городам), тогда в \
            колонки [['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0' (останутся с нулевыми \
            (по умолчанию) значениями).

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
        for index, row in tqdm(df_city_data.iterrows(), ncols=80, ascii=True,
                               desc=f'==================== Обработка данных для следующего города ===================='):

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
            data: json = self._get_no_disconnect_request(url=url_get_branches,  cookies=cookies_shops)
            # headers=self.__base_headers,  session=self.__session
            # print(f'data = {data}, {cookies_shops}')

            # Если запрос вернул None (по причине ошибок), тогда пропускаем итерацию:
            if data is None:
                continue

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

        # Удаляем дубликаты филиалов ((если хотим забрать товар из города "А", \
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

        # Получаем пути к файлам:
        dump_path = self._get_path_file_branch_dump()
        excel_path = self._get_path_file_branch_excel()

        # Сохранение exce/dump:
        self._save_data(df=df_full_branch_data, path_file_dump=dump_path, path_file_excel=excel_path)

        return df_full_branch_data
    # __________________________________________________________________ ONE_PARS_CYCLE (CATEGORY)
    def _run_one_cycle_pars(self, load_damp=True):  # get_category
        """
        Метод запуcка полного цикла парсинга (с добычей данных по API с сайта МВидео по филиалам и остатка товара
        по категориям на них) с сохранением результатов в базу данных.
        :param session:
        :type session:
        :param load_damp:  файл дампа.
        :type load_damp:
        :param imitation_ping_min: минимальная задержка
        :type imitation_ping_min: float
        :param ping_max: максимальная задержка
        :type ping_max: float
        :return: DataFrame: код магазина, категория, количество. ['id_branch','name_category','count']
        :rtype:  DataFrame
        """

        if not isinstance(load_damp, bool):
            raise ValueError('Параметр "load_damp" должен иметь тип данных bool.')

        _dump_path = self._get_path_file_branch_dump()

        # Кортеж категорий на исключение (наполнение через итерации):
        bag_category_tuple = ()

        # Создаем целевой итоговый датафрейм, куда будут сохранены данные типа: код магазина, категория (имя),
        # количество.
        df_fin_category_data = pd.DataFrame(columns=['id_branch', 'name_category', 'count', 'category_id'])

        # Включать только когда необходимо повторно собрать данные.
        if load_damp is False:

            # 1) Подготовка данных (атрибуты филиалов) для основной функции count_product_request:
            # ----------------------------------------------------------
            df_full_branch_data = self._get_branches_dat()
            if df_full_branch_data is None:
                reason = (f'Работа функции "get_shops" завершилась неудачей.')
            # pr.pprint(df_full_branch_data)
            # ----------------------------------------------------------

        # в остальных случаях загружаем дамп данных.
        elif load_damp is True:

            # _name_dump = '../data/df_full_branch_data.joblib'
            if os.path.isfile(_dump_path):  # Если файл существует, тогда: True

                # _name_dump = '../data/df_full_branch_data.joblib'
                df_full_branch_data = load(_dump_path)  # Тогда загружаем дамп
            else:
                df_full_branch_data = None
                reason = (f'Отсутствует файл дампа в директории: {_dump_path}.\n'
                          f'Запустите функцию повторно, установив параметр "load_damp: bool=False", что бы запустить '
                          f'парсинг о филиалах.\n'
                          f'Это необходимо для выполнения основного запроса к данным о количестве товара по категориям')

        # Если есть результат загрузки дампа данных по филиалам или парсинга таких данных:
        if df_full_branch_data is not None:

            # 2) Подготовка данных (очистка и иерации):
            # ----------------------------------------------------------
            # Удаляем строки, где city_id равен 0
            df_branch_not_null = df_full_branch_data[df_full_branch_data['city_id'] != 0]
            # Если нужно удалить строки в исходном DataFrame (на месте):
            # df_full_branch_data.drop(df_full_branch_data[df_full_branch_data['city_id'] == 0].index, inplace=True)

            # Создаем целевой сириес для id категорий: - лишком тяжелый, проще обычный список перебрать.
            # df_category_id_data = pd.DataFrame(CATEGORY_ID_DATA, columns=['category_id'])
            # ----------------------------------------------------------

            # 3) Основная конструкция перебирания филиалов по категориям\
            # 3.1) Итерируем по категориям (на каждую категорию итерируем по филиалам) :
            # ----------------------------------------------------------

            # for row in CATEGORY_ID_DATA:

            for row in tqdm(self._get_category_id_data(), total=len(self._get_category_id_data()), ncols=80, ascii=True,
                            desc=f'==================== Обработка данных по категории ===================='):

                time.sleep(0.1)  # \n
                # Забирает id категории:
                category_id = row

                print(f'\n==================== Категория {category_id} ====================')
                print(f'==================== Обработка данных филиалов  ====================')

                # 3.1.1) Итерируем по филиалам и по конкретной категории:
                for index, row in df_branch_not_null.iterrows():
                    # for index, row in tqdm(df_branch_not_null.iterrows(), ncols=80, ascii=True,
                    #          desc=f'=================================================================='):
                    # desc=f'==================== Обработка данных филиала ===================='):

                    # Достаем данные из строки датафрейма:
                    id_branch = row.get('id_branch')
                    city_name_branch = row.get('city_name_branch')
                    city_id = row.get('city_id')
                    region_id = row.get('region_id')
                    region_shop_id = row.get('region_shop_id')
                    timezone_offset = row.get('timezone_offset')

                    # Случайная задержка для имитации человека:
                    self._get_time_sleep_random()

                    # 3.1.1.1) Основной запрос (возвращает json (пайтон)):
                    json_python = self._count_product_request(category_id, id_branch, city_id, region_id,
                                                              region_shop_id, timezone_offset)
                    # print(json_python)
                    # ----------------------------------------------------------

                    # 4) Обработка и сохранение результатов (достаем нужные категории и сохраняем в итоговый датафрейм)
                    # ----------------------------------------------------------
                    if json_python:
                        # Обращаемся к родительскому ключу, где хранятся категории товаров:
                        all_category_in_html = json_python['body']['filters'][0]['criterias']
                        # print(f'Все категории на странице: {all_category_in_html}')

                        try:
                            # Перебираем родительскую директорию, забираем значения категорий и количество:
                            for row_category in all_category_in_html:
                                count = row_category['count']  # Количество по категории (если != 'Да' \
                                # то здесь все равно будет None, условие проверки не нужно, опускаем)

                                # Наименование категории: если count равно 'Да', то name_category также будет None
                                name_category = None if row_category['name'] == 'Да' else row_category['name']
                                # name_category = row_category['name']
                                # Наименованеи категории:

                                new_row = {'id_branch': id_branch, 'name_category': name_category, 'count': count,
                                           'category_id': category_id}

                                # print(f'count: {count}, name {name_category}')
                                print(f'{index}. {new_row}')
                                # Сохраняем в целевой итоговый датафырейм:
                                # Добавляем новую строку с помощью loc[], где индексом будет len(df_fin_category_data)
                                df_fin_category_data.loc[len(df_fin_category_data)] = new_row


                        except (KeyError, IndexError):
                            # Срабатывает, если ключ 'criterias' не существует или его невозможно получить
                            print(f'По category_id {category_id} - нет нужных тегов, пропускаем ее.')

                            # Добавление в общий кортеж багов.
                            bag_category_tuple = bag_category_tuple + (category_id,)

                    else:
                        # row_bag_iter = new_row
                        print(f'Пропуск итерации для: {id_branch} city_name_branch {city_name_branch}')
                        continue
                    break  #  Для теста - оба брейка нужны
                    # Итог код магазина, категория, количество. ['id_branch','name_category','count']
                    # ----------------------------------------------------------
                break #  Для теста - оба брейка нужны
            # Если по конкретной категории не нашлись нужные теги, такая категория добавится в список.
            # Далее эти категории можно исключить из парсинга.
            print(f'Список лишних категорий: {bag_category_tuple}.')

            # Получаем пути к файлам:
            dump_path = self._get_path_file_category_dump()
            excel_path = self._get_path_file_category_excel()
            print(f'dump_path: {dump_path}\n'
                  f'excel_path: {excel_path}')

            # # Сохраняем результат парсинга в дамп и в эксель:
            self._save_data(df=df_fin_category_data, path_file_dump=dump_path, path_file_excel=excel_path)
            # print('Результат парсинга успешно сохранен в дамп и в эксель файлы.')
            # Сохраняем в бд:
            # ----------------------------------------------------------
            # Функция сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга:
            self.load_result_pars_in_db(dump_path)


        # Парсинг остановлен по причине отсутствия файла дампа или подготовка данных в "get_shops" завершилась неудачей:
        else:
            print(f'Запуск парсинга остановлен по причине: {reason}')
            df_fin_category_data = None

        # Итог код магазина, категория, количество. ['id_branch','name_category','count']
        return df_fin_category_data
    # __________________________________________________________________
    # __________________________________________________________________ WEEK_PARS_CYCLE
    def _run_week_cycle_pars(self, day_of_week='sun', hour=23, minute=30):
        # cron_string='41 14 * * 2'):  # '0 23 * * 0'
        """
        Метод запуска полного цикла парсинга (с добычей данных по филиалам и остатка товара по категориям на них)
        с сохранением результатов в базу данных.
        0 — минута (00).
        23 — час (23:00).
        * — любой день месяца.
        * — любой месяц.
        7 — воскресенье (день недели).
        """
        # if cron_string:
        if  day_of_week and hour and minute:
            # 'Передаем ссылку на метод, а не вызываем его сразу (run_one_cycle_pars - без скобок)'
            # scheduler_instance: BlockingScheduler = self._set_schedule(self._run_one_cycle_pars, cron_string)
            scheduler_instance: BlockingScheduler = self._set_schedule(
                self._run_one_cycle_pars,
                day_of_week=day_of_week, hour=hour, minute=minute)

            print(f'Запуск по расписанию активирован. '
                  f'Ожидаемое время начала работы полного цикла парсинга:'
                  f' day_of_week: {day_of_week}, hour: {hour}, minute: {minute}.')
            scheduler_instance.start()


            # Проверяем, что задачи планировщика добавлены и планировщик готов к запуску
            # if not scheduler_instance.get_jobs():
            #     raise RuntimeError("Не удалось добавить задачу в планировщик.")
            #
            # # Запуск планировщика
            # try:
            #     scheduler_instance.start()
            # except (KeyboardInterrupt, SystemExit):
            #     print(' Остановка планировщика при выходе из программы')
            #     # Остановка планировщика при выходе из программы
            #     scheduler_instance.shutdown()
        else:
            raise ValueError(f'Ошибка в "_run_week_cycle_pars": ходные параметры не были переданы '
                             f'(day_of_week, hour, minute).')

    # __________________________________________________________________
    # ------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------

