
from parser.pars_func_request import *

# создадим словарь с перечнем url
input_list_url = {
# 'mvideo': 'https:https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205?f_category=smartfony-761&f_tolko-v-nalichii=da&f_zabrat-iz-magazina-po-adresu=A374&f_zabrat-cherez-15-minut=s984'

}


# Разбор адресной строки:
# После основного адреса ставится знак "?", далее идут только параметры (гет запрос).
# Базовый адресс: https:https://www.mvideo.ru/
# Обязательное условие 1 :  &f_tolko-v-nalichii=da&f_zabrat-iz-magazina-po-adresu=A374& , где A374 - код филиала магазина.
# Обязательное условие 2 : &f_zabrat-cherez-15-minut=s984, где s984 - геолокация





# тег содержащий количество.
# span _ngcontent-serverapp-c2232615933 class="checkbox__content"

# и span _ngcontent-serverapp-c1969068328 class="count"
# ----------------------------------------------------------------------------------------------------------------------
# Получаем первичный "суп" из тегов по ссылке (парсинг).
# soup: object = get_soup(input_list_url)
#
# print(f'Первичный суп: {soup}.')



# # Получаем список городов присутствия (парсинг).
# list: list = get_city_name_list(soup)
#
# # Получаем список url адресов филиалов (парсинг).
# city_url_list: list = get_city_url_list(soup)
#
# # Мульти-страничный поиск адресов филиалов магазинов (парсинг).
# address_list: list = get_address_list(city_url_list, corp_name_prefix=i)
#
# # - Создаем датафрейм с наименованием горов + URL
# df_city = get_df_city(city_name_list, city_url_list, corp_name_prefix=i)
# print(f'Датафрейм: "Список городов" готов!')
#
#
# print(f'Парсер завершил работу. Общее время парсинга всех корпораций составило: {m} мин. {s} сек.')

get_response()