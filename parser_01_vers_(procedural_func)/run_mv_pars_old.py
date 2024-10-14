"""Главный модуль. Запускает полный алгоритм."""
# ----------------------------------------------------------------------------------------------------------------------
import requests
# import time
import pprint
# from bs4 import BeautifulSoup as bs

from parser_02_vers.pars_func_request import *
from parser_02_vers.params_bank import *  # Все куки хедеры и параметры

pr = pprint.PrettyPrinter(indent=4, width=80, compact=False)

# Создаём сессию
session = requests.Session()

# week_ping_min
# week_ping_max
# ----------------------------------------------------------------------------------------------------------------------

#  Случайная задержка для имитации человека:
# time.sleep(random.uniform(week_ping_min, week_ping_max))

# ----------------------------------------------------------------------------------------------------------------------
# Только запуск парсинга предварительных данных
get_shops(session, CITY_DATA, imitation_ping_min = 0.5, ping_max = 1.5,
          save_name_dump='1.1._df_branch_data', save_name_excel='1.2._df_branch_data')

# ----------------------------------------------------------------------------------------------------------------------
# Раскоментировать для начала парсинга: +
df_fin_category_data = pars_cycle(session, load_damp=True, imitation_ping_min=1.5, imitation_ping_ping_max=3.5)
#
# print(df_fin_category_data)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
# Сохранить в базу данных.
# Функция сохраняет датафрейм в базу данных, предварительно загрузив дамп результатов парсинга:
# load_result_pars_in_db()
# ----------------------------------------------------------------------------------------------------------------------







# ----------------------------------------------------------------------------------------------------------------------
# -------json_python = count_product_request(
#                     session, category_id=6,
#                     id_branch='S656', city_id='CityCZ_6276', region_id='17', region_shop_id='S930', timezone_offset='5')
#
# if json_python:
#     # Обращаемся к родительскому ключу где хранятся категории товаров:
#     all_category_in_html = json_python['body']['filters'][0]['criterias']
#     # print(f'Все категории на странице: {all_category_in_html}')
#
#     # Перебираем родительскую директорию, забираем значения категорий и количество:
#     for row_category in all_category_in_html:
#         count = row_category['count']  # Количество по категории (если != 'Да' то здесь все равно будет None, \
#         # условие проверки не нужно, опускаем)
#         # Наименование категории: если count равно 'Да', то name_category также будет None
#         name_category = None if row_category['name'] == 'Да' else row_category['name'] # Наименованеи категории:
#
#
# print(f'{count}, {name_category}')