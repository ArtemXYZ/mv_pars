"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
import time
import pprint


from parser.pars_func import *
from parser.params_bank import * # Все куки хедеры и параметры

pr = pprint.PrettyPrinter(indent=4, width=80, compact=False)

# Создаём сессию
session = requests.Session()
# ----------------------------------------------------------------------------------------------------------------------






# ----------------------------------------------------------------------------------------------------------------------





# ----------------------------------------------------------------------------------------------------------------------
# Первоначальный запрос для захвата всех необходимых базовых куков: (Базовая страница).
# initial_response = session.get('https://www.mvideo.ru/', headers=headers_base)

# Задержка между запросами
# time.sleep(1)  # Задержка 1 секунды




# Запрос на извлечение всех филиалов (на вход бязательны: MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP):
# result_data = get_response('https://www.mvideo.ru/bff/region/getShops', headers=headers_base,
#                            cookies=cookies_branches, session=session)





# ------------------ Забираем наименования категорий:
# Запрос на извлечение всех категорий (на вход не бязательны куки):
result_data = get_response('https://www.mvideo.ru/bff/settings/v2/catalog', headers=headers_base,
                           cookies=None, session=session)

# Берем только категории:
categories = result_data['body']['categories']


df_categories = iterate_categories(categories)

# Сохранение DataFrame в Excel
excel_file_path = 'data/categories.xlsx'
df_categories.to_excel(excel_file_path, index=False, sheet_name='Категории')


# pr.pprint(categories)
print(df_categories)




# pr.pprint(f'Вывод: {result_data}')
# pr.pprint(categories)





# ----------------------------------------------------------------------------------------------------------------------

# # Базовая страница (посещаем для забора всех необходимых куки).
# url_base = 'https://www.mvideo.ru/'

# # Запрос на извлечение всех городов и их кодов: ! всегда одно и тоже возвращает даже с изменениями входных куки.
# result_data = get_response('https://www.mvideo.ru/bff/seo/plp/cities', headers=headers_base, cookies=cookies_city,
#                            session=session)


# Запрос на извлечение всех cookies_city_id кодов:   -  ! бессмыслено, тк необходимы все те параметрыы на вход, \
# которые мы ищем.
# result_data = get_response('https://www.mvideo.ru/bff/personalData?', headers=headers_base,
#                            cookies=cookies_city_id,  session=session)