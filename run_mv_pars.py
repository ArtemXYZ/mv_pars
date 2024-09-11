"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
# import time
import pprint


from parser.pars_func import *
from parser.params_bank import * # Все куки хедеры и параметры

pr = pprint.PrettyPrinter(indent=4, width=80, compact=False)

# Создаём сессию
session = requests.Session()
# ----------------------------------------------------------------------------------------------------------------------


url_count = 'https://www.mvideo.ru/bff/products/listing?categoryId=205&offset=0&filterParams=WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJBMzExIl0%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTA2Il0%3D'


# ----------------------------------------------------------------------------------------------------------------------




# ------------------ Забираем количество товаров по категории:
# 1 - й вариант.
# В адресной строке из списка ссылок заменяем (reff=menu_main) на  \
# (f_tolko-v-nalichii=da&f_zabrat-cherez-15-minut={s906})
# f_tolko-v-nalichii=da&f_zabrat-iz-magazina-po-adresu={A167}&f_zabrat-cherez-15-minut={s906}






# Запрос на извлечение count_product (на вход бязательны: MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
result_data = get_response(url=url_count, headers=headers_base,
                           cookies=cookies_count_product, session=session)

# pr.pprint(f'Вывод: {result_data}')
pr.pprint(result_data)





