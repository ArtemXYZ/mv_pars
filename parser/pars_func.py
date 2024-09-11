"""Основные функции вынесены в отдельный модуль."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
import pandas as pd
# from bs4 import BeautifulSoup




# from requests import Response
# from requests import

# ----------------------------------------------------------------------------------------------------------------------
def get_response(url: str, headers: dict=None, params: dict=None, cookies: dict=None, session=None) -> object:
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

        data = response.json()
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
