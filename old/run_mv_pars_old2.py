"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
# import requests
# # import time
# import pprint
# # from bs4 import BeautifulSoup as bs
#
# pr = pprint.PrettyPrinter(indent=4, width=80, compact=False)
#
# # Создаём сессию
# session = requests.Session()
# # ----------------------------------------------------------------------------------------------------------------------
#
#
# catygory_part = '/smartfony-i-svyaz-10/smartfony-205'
# branch = 'A520' # (str)
# region_shop = 's972'

# https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_tolko-v-nalichii=da&f_zabrat-iz-magazina-po-adresu=S659&f_zabrat-cherez-15-minut=s972

# url_count = 'https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_tolko-v-nalichii=da&f_zabrat-iz-magazina-po-adresu=S659&f_zabrat-cherez-15-minut=s972'
# ----------------------------------------------------------------------------------------------------------------------

# ---------------------------------------- Забираем количество товаров по категории:
# ------------- Вариант  1                 -= (ответ зашифрован, динамическая таблица)
# Забираем первичный суп по входным параметрам (для конкретной категории открываем страницу)
# soup = get_request_sup_by_html_category(branch, region_shop, category_part, session, json_type=False)


# ------------- Вариант  2
# Забираем первичный суп по входным параметрам (для конкретной категории открываем страницу)
# soup = get_undetected_sup_by_html_category(branch, region_shop, catygory_part)

# pr.pprint(soup)

# soup = html_

# Ищем первый тег <span> с классом "count"
# value = get_count_by_category(soup)
# pr.pprint(value)


# ------------- Вариант  3
# Забираем первичный суп по входным параметрам (для конкретной категории открываем страницу)
# soup = get_json_response_category_decoded_input_params(branch, region_shop, catygory_name)










# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

