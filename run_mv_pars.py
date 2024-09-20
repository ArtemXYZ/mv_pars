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
# Раскоментировать для начала парсинга: +
# df_fin_category_data = pars_cycle(session, load_damp=True, imitation_ping_min=0.5, ping_max=2.5)

# print(df_fin_category_data)

# ----------------------------------------------------------------------------------------------------------------------
# Сохранить в базу данных.
# Функция сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга:
load_result_pars_in_db()







# ----------------------------------------------------------------------------------------------------------------------
# # Забираем первичный суп по входным параметрам (для конкретной категории открываем страницу)
# soup = get_json_response_category_decoded_input_params(branch, region_shop, catygory_name)
#

# for i in result_filters_params:
#
#     a = base64_decoded(i)
#     pr.pprint(a)


# pr.pprint(f'Вывод: {result_data}')
# pr.pprint(result_data)









# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# для тестирования вариантов передачи строки параметров.
# По итогу: передачаодинакового ключа вызывает ошибку. даже если пердать в строке.
# Пока что без ошибки обрабатывается строка без ключей фильтров \
# filter_params = f'&{results_keys_value[0]}&{results_keys_value[1]}'
# def full_url(url_count, result_filters_params):
#
#     for i in result_filters_params:
#         a = i[1]
#         b = i[1]
#
#     new = f'{url_count}&{a}&{b}'
#
#     return new

# new_url = full_url(url_count, result_filters_params)


# a = '&filterParams=WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjY4Il0%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D'
# b = ('https://www.mvideo.ru/bff/products/listing?categoryId=205&offset=0&limit=24&'
#      'filterParams=WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'
#      '&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjY4Il0%3D&filter'
#      'Params=WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D')