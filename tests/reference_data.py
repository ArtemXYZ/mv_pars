



#  Нужно искать categories! ['body'][categories]
# Ответ на url_count = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0&limit=1'
json_python = {
    'success': True,
    'messages': [],
    'body': {
        'total': 0,
        'type': 'plain',
        'products': [],
        'filters': [
        ],
        'categories': [
            {
                # main_id' = '0', 'parent_id' = '0',  'id' = 31018, ///
                'id': '31018', 'count': 0, 'name': 'Товары для активного отдыха',
                'children': [
                    {
                        # main_id' = '31018', 'parent_id' = '31018',  'id' = 23715, ///
                        'id': '23715',  #
                        'count': 0,
                        'name': 'Батуты',
                        'children': [
                            {
                                # main_id' = '31018', 'parent_id' = '23715',  'id' = 23716, ///
                                'id': '23716', 'count': 0, 'name': 'Батуты', 'children': [],
                                'translitName': 'batuty', 'isSeo': True
                            },
                            {
                                # main_id' = '31018', 'parent_id' = '23715',  'id' = 35546, ///
                                'id': '35546', 'count': 0, 'name': 'Крышы для батутов',
                                'children': [], 'translitName': 'kryshy-dlya-batutov',
                                'isSeo': True
                            },
                            {
                                'id': '33766', 'count': 0, 'name': 'Лестницы для батутов',
                                'children': [], 'translitName': 'lestnicy-dlya-batutov',
                                'isSeo': True
                            },
                            {
                                'id': '33891', 'count': 0, 'name': 'Чехлы для батутов',
                                'children': [], 'translitName': 'chehly-dlya-batutov',
                                'isSeo': True
                            },
                            {
                                'id': '35316', 'count': 0, 'name': 'Мелки для батутов',
                                'children': [], 'translitName': 'melki-dlya-batutov',
                                'isSeo': True
                            },
                            {
                                'id': '35547', 'count': 0,
                                'name': 'Колья для крепления батута',
                                'children': [],
                                'translitName': 'kolya-dlya-krepleniya-batuta',
                                'isSeo': True
                            }
                        ],
                        'translitName': 'batuty',
                        'urlFacetCrossBlock': None}
                ],
                'translitName': 'tovary-dlya-aktivnogo-otdyha'}
        ],
        'selected_categories_ids': ['23716']
    }
}


#  +
print(f'{json_python['body']['categories']}')

# +
print(f'selected_categories_ids: {json_python['body']['selected_categories_ids']}')


url_sitemap = 'https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml'

# (такие-то есть категории, но не все. Мало)
url_count_settings = f'https://www.mvideo.ru/bff/settings?types=plp'

# (похоже, что здесь все категории, но метод POST)
url_count_settings = f'https://www.mvideo.ru/bff/product-details/list'

url = 'https://www.mvideo.ru/bff/settings/v2/catalog'
# Структура:
# Айди категории: json_python['body']['products']['categories']['id']
# Имя категории: json_python['body']['products']['categories']['name']
# Имя категории: json_python['body']['products']['groups']['name']

# @staticmethod
# def xml_teg_grabber(self, row_xml: bytes, xml_tags_by_pars: dict):
#     """
#         Метод обработки xml файлов.
#         Принимает xml в байт-формате (data = response.content), разбирает информацию по переданному тегу.
#     """


# category_id = 205
# MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET
# url_new_construct = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0'

# ендпоинт.
# url_new = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds=205&offset=0'
#
# url_new_all_params = 'https://www.mvideo.ru/bff/products/v2/search?categoryIds=205&offset=0&filterParams=WyLQotC%2B0LvRjNC60L4g0L\
# Ig0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiL\
# CItMTEiLCJTOTcyIl0%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMT\
# IiLCJTNjU5Il0%3D&doTranslit=false&limit=48&context=v2dzaG9wX2lkZFM5NzJsY2F0ZWdvcnlfaWRzn2MyMDX%2FZmNhdF9JZGMyMDX%2F'
#
# # Значение переменной: ["Только в наличии","-9","Да"]
# url_new_params_1 = 'WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'
#
# # filterParams: ["Забрать через 15 минут","-11","S972"]
# url_new_params_2 = 'WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D'
#
# # filterParams: ["Забрать из магазина по адресу","-12","S659"]
# url_new_params_3 = (f'WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90'
#                     f'LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjU5Il0%3D')
#
# url_new_params_4 = 'doTranslit=false'
# url_new_params_5 = 'limit=48'
#
# # &context= : Ошибка декодирования: 'utf-8' codec can't decode byte 0xbf in position 0: invalid start byte
# url_new_params_6 = 'v2dzaG9wX2lkZFM5NzJsY2F0ZWdvcnlfaWRzn2MyMDX%2FZmNhdF9JZGMyMDX%2F'




# url_new_params_decoded = _base64_decoded(url_new_params_2)
# print(url_new_params_decoded)  # ["Только в наличии","-9","Да"]


# Базовая строка подключения:
# url_count = f'https://www.mvideo.ru/bff/products/listing?categoryId={category_id}&offset=0&limit=1'
# categoryId - обязательно
#
# # Конструктор куков:
# cookies_count_product = {
#     'MVID_CITY_ID': city_id,
#     'MVID_REGION_ID': region_id,
#     'MVID_REGION_SHOP': region_shop_id,
#     'MVID_TIMEZONE_OFFSET': timezone_offset,
# }
#
# # Полная строка с фильтрами:
# full_url = f'{url_count}{result_filters_params}'
# # --------------------------------------- Переменные:


# def _base64_decoded(url_param_string):
#     """
#         Расшифровка параметров URL.
#         :param url_param_string: (base64_string)
#         :type url_param_string:
#         :return:
#         :rtype:
#     """
#     try:
#         # Шаг 1: URL-декодирование
#         url_param_string_decoded = urllib.parse.unquote(url_param_string)
#         # Шаг 2: Base64-декодирование
#         base64_decoded_string = base64.b64decode(url_param_string_decoded).decode('utf-8')
#         return base64_decoded_string
#     except Exception as e:
#         print(f'Ошибка декодирования: {e}')
#         return None