"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
import requests

from parser.pars_func import *
from parser.headers_bank import *


# Создаём сессию
session = requests.Session()
# ----------------------------------------------------------------------------------------------------------------------




cookies = {
    "MVID_CITY_ID": "CityCZ_6276",
    "MVID_REGION_ID": "17",
    # другие cookies, которые могут быть необходимы
    "MVID_REGION_SHOP": "S930",
    "MVID_CITY_CHANGED": "true"
}

# ----------------------------------------------------------------------------------------------------------------------













# ----------------------------------------------------------------------------------------------------------------------
# Первоначальный запрос для захвата всех необходимых базовых куков: (Базовая страница).
initial_response = session.get('https://www.mvideo.ru/', headers=headers_base)


# Запрос на извлечение всех филиалов
result_data = get_response('https://www.mvideo.ru/bff/region/getShops', headers=headers_base, cookies=cookies,
                           session=session)

print(result_data)


# # Базовая страница (посещаем для забора всех необходимых куки).
# url_base = 'https://www.mvideo.ru/'