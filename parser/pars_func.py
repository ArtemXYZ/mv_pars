"""Основные функции вынесены в отдельный модуль."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
# from bs4 import BeautifulSoup
# import time



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
    if cookies:
        session.cookies.update(cookies)

    # Обычный запрос или сессия:
    if session:
        response = session.get(url, headers=headers, params=params)

    else:
        response = requests.get(url, headers=headers, params=params)


    # Выполнение запроса:
    if response.status_code == 200:

        data = response.json()
        # print(f'{data}')

    else:
        data = None
        print(f"Ошибка: {response.status_code}")

    return data












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
