"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
# import time
import pprint
# from bs4 import BeautifulSoup as bs

from parser.pars_func_request import *
from parser.params_bank import *  # Все куки хедеры и параметры

pr = pprint.PrettyPrinter(indent=4, width=80, compact=False)

# Создаём сессию
session = requests.Session()

# ----------------------------------------------------------------------------------------------------------------------

# catygory_part = '/smartfony-i-svyaz-10/smartfony-205'
# branch = 'A520' # (str)
# region_shop = 's972'


# ----------------------------------------------------------------------------------------------------------------------
 # Забираем количество товаров по категории: Вариант  3
category_name = 'Мобильные устройства'
region_shop_code = 'S972'
branch_code = 'S668'
# ---------------- Самара
city_id = 'CityCZ_1780'
region_id = '4'
time_zone = '4'

categoryId = '205'
url_count = f'https://www.mvideo.ru/bff/products/listing?categoryId={categoryId}&offset=0'  # categoryId - обязательно

cookies_count_product = {
    'MVID_CITY_ID': city_id,
    'MVID_REGION_ID': region_id,
    'MVID_REGION_SHOP': region_shop_code,
    'MVID_TIMEZONE_OFFSET': time_zone,
}
# ---------------------------------------- Параметры фильтрации в запросе:

# Формирование закодированных параметров фильтрации:
result_filters_params = encoded_request_input_params(category_name, region_shop_code, branch_code)


# ---------------------------------------- Выполняем основной запрос:

# Запрос на извлечение count_product (на вход бязательны: \
# MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
result_data = get_response(url=url_count, headers=headers_base, params=result_filters_params, - косяк в result_filters_params
                           cookies=cookies_count_product, session=session)





# ----------------------------------------------------------------------------------------------------------------------
# # Забираем первичный суп по входным параметрам (для конкретной категории открываем страницу)
# soup = get_json_response_category_decoded_input_params(branch, region_shop, catygory_name)
#








# pr.pprint(f'Вывод: {result_data}')
pr.pprint(result_data)









# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

