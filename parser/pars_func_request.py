"""Основные функции вынесены в отдельный модуль."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
import pandas as pd
from pandas import DataFrame
import time
import random
import json

import base64
import urllib.parse

from bs4 import BeautifulSoup

from parser.params_bank import * # Все куки хедеры и параметры


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
def get_count_by_category(soup: BeautifulSoup) -> list[str] | None:

    # Ищем первый тег <span> с классом "count"
    # span_tag = soup.find('span', class_=['count', 'ng-star-inserted'])

    span_tag = soup.find('div' ,  class_='app')

    # Примеры:
    # span_tag = soup.find('h1')   #.text
    # _ngcontent - serverapp - c2525370525
    # results = soup.find("div", {"class": "app", "style":
    # "background:#f9f9f9;padding:20px;"}).find_all("a")

    # print(span_tag)

    if span_tag:
        value = span_tag.get_text(strip=True)  # Убирает лишние пробелы

    else:
        value = None



    return span_tag  # value

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






def encoded_request_input_params(category_name: str, region_shop_code: str, branch_code: str):

    """
     url_list = {
    'filterParams': ["Мобильные устройства", "-12", "A311"],
    'filterParams': ["Мобильные устройства", "-11", "S906"],}

    category_name = 'Мобильные устройства'
    region_shop_code = 'S906'
    branch_code = 'A311'

    """

    results_keys_value = []

    # 1. Формирование фильтров:
    filter_param_11 = [category_name, '-11', region_shop_code]
    filter_param_12 = [category_name, '-12', branch_code]

    filter_tuple = (filter_param_11, filter_param_12)


    # 2. Кодирование:
    for param_list in filter_tuple:

        encoded_list = str(param_list).encode('utf-8')  # Преобразуем списки в строку и кодируем в 'utf-8':
        base64_encoded = base64.b64encode(encoded_list).decode('utf-8')  # Base64-кодирование
        # print(f"Base64-кодированная строка: {base64_encoded}")
        final_encoded = urllib.parse.quote(base64_encoded)  # URL-кодирование
        # print(f"Итоговый URL-кодированный параметр: {final_encoded}")



        # 3. Сохраняем в виде словаря для передачи как параметр в строку запроса.
        # Добавляем в список результат кодирования:
        results_keys_value.append(final_encoded)  # Ожидаем на выход: [рез1, рез2]
        # print(results_keys_value)

    # filter_params = {
    #     'filterParams1': results_keys_value[0],
    #     'filterParams2': results_keys_value[1],
    # }

    # Одинаковый ключ:
    filter_params = [
        ('filterParams', results_keys_value[0]),
        ('filterParams', results_keys_value[1]),
    ]

    return filter_params






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
