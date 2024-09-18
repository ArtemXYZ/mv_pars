"""Списки данных для различных запросов"""

headers_base = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.mvideo.ru/',
    'Origin': 'https://www.mvideo.ru',
}


# https://www.mvideo.ru/bff/region/getShops  +
# cookies_branches = {
#     "MVID_CITY_ID": "CityCZ_6276",
#     "MVID_REGION_ID": "17",
#     "MVID_REGION_SHOP": "S930",
# }

# cookies_count_product = {
#     'MVID_CITY_ID': 'CityCZ_2534',
#     'MVID_REGION_ID': '10',
#     'MVID_REGION_SHOP': 'S906',
#     'MVID_TIMEZONE_OFFSET': '5',
# }



# https://www.mvideo.ru/bff/region/getShops  +
CITY_DATA = [
    ('Бузулук',	'CityDE_31010',	'4', 'S972', '4'),
    ('Новокуйбышевск', 'CityCZ_3744', '4', 'S972', '4'),
    ('Самара', 'CityCZ_1780', '4', 'S972', '4'),
    ('Бирск', 'CityDE_27142', '10', 'S906', '5'),
    ('Благовещенск', 'CityDE_27146', '10', 'S906', '5'),
    ('Стерлитамак', 'CityR_60', '10', 'S906', '5'),
    ('Уфа', 'CityCZ_2534', '10', 'S906', '5'),
    ('Вольск', 'CityDE_31342', '13', 'S908', '4'),
    ('Маркс', 'CityDE_31350',  '13', 'S908', '4'),
    ('Саратов', 'CityCZ_984', '13', 'S908', '4'),
    ('Энгельс', 'CityCZ_2714', '13', 'S908', '4'),
    ('Оренбург', 'CityCZ_6276', '17', 'S930', '5'),
    ('Тольятти', 'CityCZ_6270', '24', 'S924', '4'),
    # ('Белорецк', 'CityDE_27134', '27', 'S966', '5'),
    ('Ишимбай', 'CityDE_27162',  '58', 'S983', '5'),
    ('Салават', 'CityR_58', '58', 'S983', '5'),
    ('Пенза', 'CityCZ_7182', '59', 'S922', '3'),
    ('Сызрань', 'CityR_109', '75', 'S941', '4'),
    ('Белебей', 'CityDE_27122', '88', 'S984', '5'),
    ('Октябрьский', 'CityCZ_15514', '88', 'S984', '5'),
    ('Туймазы', '24300007', '88', 'S984', '5'),
    ('Новотроицк', 'CityR_70', '99',  'S938', '5'),
    ('Орск', 'CityCZ_15549', '99', 'S938', '5'),
    # ('Сыктывкар', 'CityR_102', '102', 'S964', '3'),
    ('Балаково', 'CityR_91', '13', 'S908', '4')
]

CATEGORY_ID_DATA: tuple = ('205',

)

# ---------------- Самара
# category_id = '205'
# city_id = 'CityCZ_1780'
# region_shop_id = 'S972'
#
# branch_code = 'S668'
# region_id = '4'
# time_zone = '4'

#
# https://www.mvideo.ru/sitebuilder/blocks/browse/store/locator/store.json.jsp?storeId=S103&hideBtn=true&skuId=


# не работающие / неактуальные запросы
# ----------------------------------------------------------------------------------------------------------------------
# # https://www.mvideo.ru/bff/seo/plp/cities
# cookies_city = {
#     "MVID_CITY_ID": "CityCZ_2534",
#     "MVID_REGION_ID": "10",
#     "MVID_REGION_SHOP": "s906",
#     "MVID_TIMEZONE_OFFSET": "5",
# }

# # https://www.mvideo.ru/bff/personalData?
# cookies_city_id = {
#     'MVID_REGION_ID': '13',
#     'MVID_REGION_SHOP': 'S908',
#     "MVID_CITY_ID": "CityCZ_984",
#     'MVID_TIMEZONE_OFFSET': '4',
# }