"""Основные функции вынесены в отдельный модуль."""
# ----------------------------------------------------------------------------------------------------------------------
import selenium
# import pandas as pd
import time
import random
import undetected_chromedriver

# from bs4 import BeautifulSoup

from selenium import webdriver  # https://github.com/jsnjack/chromedriver/releases/tag/v121.0.6167.184
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import json

from parser.params_bank import * # Все куки хедеры и параметры
# from run_mv_pars import session

# from requests import Response
# from requests import

# ----------------------------------------------------------------------------------------------------------------------
driver_path = 'C:\\Users\\Poznyishev.AA\\Documents\\00_Проекты_Пайтон\\MV_pars\\driver\\chromedriver.exe'
# driver_path = '../driver/chromedriver.exe'

# # Создаем объект Service
# service = Service(executable_path=driver_path)
#
# # Установка User-Agent
# chrome_options = Options()
# chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.86 Safari/537.36")
# chrome_options.add_argument("--disable-blink-features=Automation Controller")

# Устанавливаем путь к драйверу браузера
# driver = webdriver.Chrome(service=service, options=chrome_options)

# -------------------------------------

# Устанавливаем путь к драйверу браузера
driver_und = undetected_chromedriver.Chrome(version_main=121)

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




# Рекурсивная функция для обхода всех категорий
def iterate_categories(categories, start_lvl=0, parent_lvl='main'):

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
def get_recuest_sup_by_html_category(branch, region_shop, catygory_part, session, json_type):
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

# -----------------------------------------------------------------------
# Получаем количество тавара по категориям (через селениум):
def get_selenium_sup_by_html_category(branch, region_shop, catygory_part):
    """
    Этот код ищет span с текстом "count_value", который находится внутри div с классом plp__current-category.

    Ищем div с классом plp__current-category, который содержит целевой span с классами count и ng-star-inserted.
    Используем > для поиска дочернего элемента span внутри этого div.
    WebDriverWait: Ожидаем, пока элемент не появится в DOM.
    """
    # ------------------------------------ Шаблоны:
    url_base = 'https://www.mvideo.ru'

    # Динамически изменяемые параметры.
    full_url_no_param = (f'{url_base}{catygory_part}?'
                         f'f_tolko-v-nalichii=da&'
                         f'f_zabrat-iz-magazina-po-adresu={branch}&'
                         f'f_zabrat-cherez-15-minut={region_shop}'
                         )

    # driver.implicitly_wait(10)  # Добавление общего неявного ожидания




    # Явное ожидание, пока элемент с классом "count ng-star-inserted" станет доступным
    # try:

        # Запрос на извлечение сраницы:
        # driver.get(url=full_url_no_param)  # html =


    with driver_und as driver_und:
        driver_und.get(full_url_no_param)

        # time.sleep(5)  # Задержка 1 секунды
        # Выполнение случайных задержек
        time.sleep(random.uniform(1.0, 3.0))

        # # # Поиск <div> с классом "plp__current-category ng-star-inserted", внутри которого находится <span> с текстом
        # div_tag = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "div.plp__current-category.ng-star-inserted")))
        #
        #
        #
        #
        # # # Теперь ищем внутри этого div нужный <span> с классом count.ng-star-inserted
        # # # Ожидание, пока <span> станет видимым
        # span_tag = WebDriverWait(driver, 5).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "span.count.ng-star-inserted")))



        # ------------------- не сработали варианты
        # result = driver.find_element(By.ID, "62f43af5e9824e529e436e429d0749d7") - ошибка не находит
        # result = driver.find_element(By.CSS_SELECTOR, "span.count.ng-star-inserted") - ошибка не находит
        # span_tag = WebDriverWait(driver, 7).until(
        #     EC.visibility_of_element_located((By.CSS_SELECTOR, "span.count.ng-star-inserted"))) - ошибка не находит
        # span_tag = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "span.count.ng-star-inserted")))
        # div_tag = WebDriverWait(driver, 5).until(
        #     EC.presence_of_element_located((By.CSS_SELECTOR, "span.count.ng-star-inserted")))

        # Получаем текст элемента
        # count_value = span_tag.text



        # print(f"Значение: {span_tag.text}")

    # finally:

        # time.sleep(2)  # Задержка 1 секунды
        # Закрытие браузера
        # driver_und.close()
        # driver_und.quit()

    #

    # result = driver.find_element(By.CLASS_NAME, "count.ng-star-inserted")  # ng-star-inserted
    # Используем CSS-селектор для поиска элемента с несколькими классами
    # result = driver.find_element(By.CSS_SELECTOR, ".count.ng-star-inserted")


    # return count_value







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




# 3 й вариант
def get_json_response_category_decoded_input_params(branch, region_shop, catygory_name):

    MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET

    cookies_count_product = {
        'MVID_CITY_ID': 'CityCZ_2534',
        'MVID_REGION_ID': '10',
        'MVID_REGION_SHOP': 'S906',
        'MVID_TIMEZONE_OFFSET': '5',
    }

    # Запрос на извлечение count_product
    # (на вход бязательны:  ):
    result_data = get_response(url=url_count, headers=headers_base, params=cherez_15_minut,
                               cookies=cookies_count_product, session=session)




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
