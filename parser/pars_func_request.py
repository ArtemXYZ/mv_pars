"""Основные функции вынесены в отдельный модуль."""
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

from tqdm import tqdm

from parser.params_bank import * # Все куки хедеры и параметры
from settings.configs import engine_mart_sv

# from requests import Response
# from requests import

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
def get_response(url: str, headers: dict=None, params: dict=None, cookies: dict=None, session=None,
                 json_type=True) -> object:
    """
    Универсальная функция для запросов с передаваемыми параметрами.
    :param url:
    :type url:
    :param headers:
    :type headers:
    :param params:
    :type params:
    :param cookies:
    :type cookies:
    :param session:
    :type session:
    :return:
    :rtype:
    """


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
            # print(f'{data}')

    else:
        data = None
        print(f"Ошибка: {response.status_code} - {response.text}")

    return data


# Рекурсивная функция для обхода всех категорий (в файле json):
def iterate_categories(categories, start_lvl=0, parent_lvl='main') -> DataFrame:

    df_categories = pd.DataFrame(columns=['lvl', 'category_name', 'URL' ])
    # ['lvl', 'main_category_name','sub_category_name_1', 'URL' ])



    # Далее итерируем по ним:
    for count, category in enumerate(categories, start=start_lvl):
    # for category in categories:

        # # Если есть уровень, тогда ссуммируем его
        # if next_lvl:
        #     start_namb = next_lvl + category
        #
        # else:
        #     start_namb = 1


        # Извлекаем name и url
        get_name = category.get('name')
        get_url = category.get('url')

        # get_lvl = f'{count}_{parent_lvl}'
        get_lvl = f'{parent_lvl}'

        # -------------- главная категория:
        # Добавляем записи в DataFrame (главная категория):
        df_categories.loc[len(df_categories.index )] = [get_lvl, get_name, get_url]


        # -------------- подкатегория:
        # Если есть вложенные категории, продолжаем обход
        subcategories = category.get('categories', [])
        if subcategories:
            # Рекурсивно обходим подкатегории, увеличивая уровень:
            df_subcategories = iterate_categories(subcategories, start_lvl=1, parent_lvl=get_name) #
            # Объединяем результат с текущим DataFrame
            df_categories = pd.concat([df_categories, df_subcategories], ignore_index=True)

    return df_categories


# Получаем количество тавара по категориям (через реквест):
def get_request_sup_by_html_category(branch, region_shop, catygory_part, session, json_type):
    """Возвращает первичный суп из тегов или json если json_type=True"""
    # ------------------------------------ Шаблоны:
    url_base = 'https://www.mvideo.ru'

    full_url_no_param = f'{url_base}{catygory_part}?'
    # Динамически изменяемые параметры.
    param_filter = {'f_tolko-v-nalichii': 'da',
                    'f_zabrat-iz-magazina-po-adresu': f'{branch}',
                    'f_zabrat-cherez-15-minut': f'{region_shop}',
                    }

    # ------------------------------------

    # Запрос на извлечение sup_count_product:
    result = get_response(url=full_url_no_param, headers=headers_base, params=param_filter,
                               cookies=None, session=session, json_type=json_type)

    # Исключаем ошибку, если вдруг забыли передать параметр (json_type=не json):
    if json_type is False:
        result = BeautifulSoup(result, "html.parser")  # soup
    else:
        result

    return result


# Разбираем суп из тегов, ищем количество для категории:
# def get_count_by_category(soup: BeautifulSoup) -> list[str] | None:
#
#     # Ищем первый тег <span> с классом "count"
#     # span_tag = soup.find('span', class_=['count', 'ng-star-inserted'])
#
#     span_tag = soup.find('div' ,  class_='app')
#
#     # Примеры:
#     # span_tag = soup.find('h1')   #.text
#     # _ngcontent - serverapp - c2525370525
#     # results = soup.find("div", {"class": "app", "style":
#     # "background:#f9f9f9;padding:20px;"}).find_all("a")
#
#     # print(span_tag)
#
#     if span_tag:
#         value = span_tag.get_text(strip=True)  # Убирает лишние пробелы
#
#     else:
#         value = None
#
#
#
#     return span_tag  # value

    # list_city: list[str] = []  # Создаем пустой список, в него поместим результат работы цикла


# 3 й вариант -- !
# def get_json_response_category_decoded_input_params(param_cod):
#
#     #
#
#     cookies_count_product = {
#         'MVID_CITY_ID': 'CityCZ_2534',
#         'MVID_REGION_ID': '10',
#         'MVID_REGION_SHOP': 'S906',
#         'MVID_TIMEZONE_OFFSET': '5',
#     }
#
#     # Запрос на извлечение count_product
#     # (на вход бязательны:  ):
#     result_data = get_response(url=url_count, headers=headers_base, params=param_cod,
#                                cookies=cookies_count_product, session=session)


def base64_decoded(url_param_string):
    """
    Расшифровка параметров URL.
    :param base64_string:
    :type base64_string:
    :return:
    :rtype:
    """
    try:

        # Шаг 1: URL-декодирование
        url_param_string_decoded = urllib.parse.unquote(url_param_string)

        # Шаг 1: Дополнение выравнивания строки
        # padding = len(base64_string) % 4
        # if padding:
        #     base64_string += '=' * (4 - padding)


        # Шаг 2: Base64-декодирование
        base64_decoded_string = base64.b64decode(url_param_string_decoded).decode('utf-8')

        return base64_decoded_string
    except Exception as e:
        print(f'Ошибка декодирования: {e}')
        return None


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

    # ----------------  Не работает если ожидаем (пердаем) одинаковые ключи ("&filterParams=...24&filterParams=... " )
    # filter_params = {
    #     'filterParams1': results_keys_value[0],
    #     'filterParams2': results_keys_value[1],
    # }

    # Одинаковый ключ: Не все сервисы корректно принимают параметры с одинаковыми ключами. \
    # # Хотя requests корректно формирует URL с повторяющимися параметрами, сервер может их неправильно обрабатывать.
    # filter_params = [
    #     ('filterParams', results_keys_value[0]),
    #     ('filterParams', results_keys_value[1]),
    # ]
    # ----------------

    # filter_params = f'&{results_keys_value[0]}&{results_keys_value[1]}' - не работает при передаче в параметры \
    # реквест, однако ошибку не вызывает.

    filter_params = (results_keys_value[0], results_keys_value[1], results_keys_value[2])
    filter_params = (f'&filterParams={results_keys_value[0]}'
                     f'&filterParams={results_keys_value[1]}'
                     f'&filterParams={results_keys_value[2]}')

    return filter_params


 # Забираем количество товаров по категории: Вариант  3
def count_product_request(session, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset):

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
    result_filters_params = encoded_request_input_params(id_branch, region_shop_id)

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
    data = get_response(url=full_url, headers=headers_base, params=None,  # косяк в result_filters_params
                               cookies=cookies_count_product, session=session)

    return data


def get_shops(session, CITY_DATA: list[tuple], imitation_ping_min: float = 0.5, ping_max: float = 1.5,
              save_name_dump='df_full_branch_data', save_name_excel='df_full_branch_data'):
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
    :return: DataFrame: ['id_branch', 'city_name_branch', , 'address_branch', 'city_id', 'region_id', 'region_shop_id',
                'timezone_offse'];
            Если в CITY_DATA не найдется исходного города (исходные данные для целевых запросов по городам), тогда в \
            колонки [['city_id', 'region_id', 'region_shop_id', 'timezone_offset']] = '0' (останутся с нулевыми \
            (по умолчанию) значениями).

    :rtype:  DataFrame
    """

    _name_dump = f'../data/{save_name_dump}.joblib'
    _name_excel = f'../data/{save_name_excel}.xlsx'

    # -----------------------------------
    # Запрос на коды магазинов и адреса. Необходимо передать куки.
    url = "https://www.mvideo.ru/bff/region/getShops"
    # -----------------------------------

    # Отмена: Переделать! не нужно создавать датафрейм для переборки, \
    # Отмена:  однако при обращении к элементам картежа - проверку на нул! \
    # Причина: в конце функции проще искать через пандас нужные значения в CITY_DATA.

    # 1. Преобразуем список картежей CITY_DATA в датафрейм:
    df_city_data = pd.DataFrame(CITY_DATA, columns=['city_name', 'city_id', 'region_id', 'region_shop_id',
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

        city_id = row.get('city_id')  #  row['city_id']
        region_id = row.get('region_id')        # row['region_id']
        region_shop_id = row.get('region_shop_id')   # row['region_shop_id']
        time_zone = row.get('timezone_offset')
        city_name_parent = row.get('city_name')

        # print(f'\n'
        #       f'Город (parent) {index} : {city_name_parent}')

        # 4. Конструктор куков:
        cookies_shops = {'MVID_CITY_ID': city_id, 'MVID_REGION_ID': region_id, 'MVID_REGION_SHOP': region_shop_id,
                         'MVID_TIMEZONE_OFFSET': time_zone}

        # 5. Случайная задержка для имитации человека:
        time.sleep(random.uniform(imitation_ping_min, ping_max))

        # 6. Выполняем основной запрос на извлечение филиалов в конкретном городе:
        # (на вход бязательны: # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
        data: json = get_response(url=url, headers=headers_base, cookies=cookies_shops, session=session)
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


def pars_cycle(session, load_damp: bool=True, imitation_ping_min: float = 0.5, imitation_ping_ping_max: float = 2.5,
               save_name_dump='df_full_branch_data', save_name_excel='df_full_branch_data'):

    """
    Итоговая функция полного цикла обработки (сбора с сайта МВидео)
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

    _name_dump = f'../data/{save_name_dump}.joblib'
    _name_excel = f'../data/{save_name_excel}.xlsx'

    # Кортеж категорий на исключяение (наполнение через итерации):
    bag_category_tuple = ()

    # Создаем целевой  итоговый датафрейм, куда будут сохранены данные типа: код магазина, категория (имя), количество.
    df_fin_category_data = pd.DataFrame(columns=['id_branch','name_category','count', 'category_id'])

    # Bключать только когда необходимо повторно собрать данные.
    if load_damp is False:

        # 1) Подготовка данных (атрибуты филиалов) для основной функции count_product_request:
        # ----------------------------------------------------------
        df_full_branch_data = get_shops(session, CITY_DATA, imitation_ping_min=imitation_ping_min ,
                                        imitation_ping_ping_max=imitation_ping_ping_max,
                                        save_name_dump=save_name_dump, save_name_excel=save_name_excel)
        if df_full_branch_data is None:
            reason = (f'Работа функции "get_shops" завершилась неудачей.')
        # pr.pprint(df_full_branch_data)
        # ----------------------------------------------------------

    # в остальных случаях загружаем дамп данных.
    elif load_damp is True:

        # _name_dump = '../data/df_full_branch_data.joblib'
        if os.path.isfile(_name_dump):  # Если файл существует,тогда: True

            # _name_dump = '../data/df_full_branch_data.joblib'
            df_full_branch_data = load(_name_dump)  # Тогда загружаем дамп
        else:
            df_full_branch_data = None
            reason =(f'Отсутствует файл дампа в директории: "/data/df_full_branch_data.joblib".\n'
                     f'Запустите функцию повторно, установив параметр "load_damp: bool=False", что бы запустить '
                     f'парсинг о филиалах.\n'
                     f'Это необходимо для выполнения основного ззапроса к данным о количестве товара по категориям')


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

        for row in tqdm(CATEGORY_ID_DATA,  total=len(CATEGORY_ID_DATA), ncols=80, ascii=True,
                        desc=f'==================== Обработка данных по категории ===================='):

            time.sleep(0.1) #\n
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
                time.sleep(random.uniform(imitation_ping_min, imitation_ping_ping_max))

                # 3.1.1.1) Основной запрос (возвращает json (айтон)):
                json_python = count_product_request( # address_branch - пока не нужен. city_name_branch,
                    session, category_id,
                    id_branch, city_id, region_id, region_shop_id, timezone_offset)
                # print(json_python)
        # ----------------------------------------------------------


                # 4) Обработка и сохранение результатов (достаем нужные категории и сохраняем в итоговый датафрейм)
                # ----------------------------------------------------------
                if json_python:
                    # Обращаемся к родительскому ключу где хранятся категории товаров:
                    all_category_in_html = json_python['body']['filters'][0]['criterias']
                    # print(f'Все категории на странице: {all_category_in_html}')

                    try:

                        # Перебираем родительскую директорию, забираем значения категорий и количество:
                        for row_category in all_category_in_html:
                            count = row_category['count']  # Количество по категории (если != 'Да' \
                            # то здесь все равно будет None,  условие проверки не нужно, опускаем)

                            # Наименование категории: если count равно 'Да', то name_category также будет None
                            name_category = None if row_category['name'] == 'Да' else row_category['name']
                            # name_category = row_category['name']
                            # Наименованеи категории:

                            new_row = {'id_branch': id_branch, 'name_category': name_category, 'count': count,
                                       'category_id': category_id}

                            # print(f'count: {count}, name {name_category}')
                            print(#f'\n'
                                  f'{index}. {new_row}')
                            # Сохраняем в целевой итоговый датафырейм:
                            # Добавляем новую строку с помощью loc[], где индексом будет len(df_fin_category_data)
                            df_fin_category_data.loc[len(df_fin_category_data)] = new_row


                        # break
                    except (KeyError, IndexError):
                        # Срабатывает, если ключ 'criterias' не существует или его невозможно получить
                        print(f'По category_id {category_id} - нет нужных тегов, пропускаем ее.')

                        # Добавление в общий кортеж багов.
                        bag_category_tuple =  bag_category_tuple + (category_id,)

                # time.sleep(0.1)

            # time.sleep(0.1)
                # Итог код магазина, категория, количество. ['id_branch','name_category','count']
                # ----------------------------------------------------------

        # Если по конкретной категории не нашлись нужные теги, такая категория добавится в стписок. Далее эти категории
        # можно исключить из парсинга.
        print(f'Список лишних категорий: {bag_category_tuple}.')

        # Сохраняем результат парсинга в дамп и в эксель:
        dump(df_fin_category_data, _name_dump) # _name_dump = '../data/df_full_branch_data.joblib'
        df_fin_category_data.to_excel(_name_excel, index=False, )   # _name_excel = '../data/df_full_branch_data.xlsx'

        # Сохраняем в бд:
        # ----------------------------------------------------------
        # Функция сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга:
        load_result_pars_in_db()



    # Парсинг остановлен по причине отсутствия файла дампа или подготовка данных в "get_shops" завершилась неудачей:
    else:
        print(f'Запуск парсинга остановлен по причине: {reason}')
        df_fin_category_data = None



    # Итог код магазина, категория, количество. ['id_branch','name_category','count']
    return df_fin_category_data


# Функция сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга:
def load_result_pars_in_db():


    # ------------------------------------ Загрузка дампа результатов парсинга ------------------------------------
    if os.path.isfile('../data/df_fin_category_data.joblib'):  # Если файл существует,тогда: True

        # ------------------------------------
        load_damp_df = load('../data/df_fin_category_data.joblib')  # Тогда загружаем дамп
        print("Дамп успешно загружен!")

        current_time  = datetime.now()


        # Форматируем время в строку
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        # Добавляем новые колонки со значением 0:
        load_damp_df['dt_load'] = formatted_time
        # print(load_damp_df)
        # ------------------------------------
        print("Соединение с сервером для загрузки.")
        # ------------------------------------
        # Загрузка итогового DataFrame в базу данных:
        load_damp_df.to_sql(name='current_stock_mvideo', schema='inlet', con=engine_mart_sv,
                            if_exists='replace', index=False, method='multi')
        # Выбираем метод 'replace' для перезаписи таблицы или 'append' для добавления данных
        # method='multi' используется для оптимизации вставки большого объема данных.

        # Закрытие соединения
        engine_mart_sv.dispose()

        print("Данные успешно сохранены в базу данных!")



    else:
        load_damp_df = None
        print(f'Отсутствует файл дампа "df_fin_category_data" в директории: "/data/df_full_branch_data.joblib"!')

# ----------------------------------------------------------------------------------------------------------------------
# def get_soup(url: str = None) -> object:
#     """Получаем первичный "суп" из тегов по ссылке с помощью BeautifulSoup4.
#
#       :param url: Начальный адрес веб-страницы для запуска парсинга, defaults to None
#       :type url: str
#       :raises ValueError: Неверное значение переменной, проверьте тип данных (необходимый тип: str)
#       :rtype: object
#       :return: Подготовка первичных данных для парсинга филиалов магазинов бытовой техники.
#
#       """
#
#     if url is not None:
#         page: Response = requests.get(url)  # При помощи requests.get мы совершаем запрос к веб страничке.
#         soup: BeautifulSoup = BeautifulSoup(page.content, "html.parser")
#         # Сама функция возвращает ответ от сервера (200, 404 и т.д.),
#         # а page.content предоставляет нам полный код загруженной страницы.
#         # Возвращаемое значение: первичный "суп" из тегов.
#     else:
#         return None
#     return soup
