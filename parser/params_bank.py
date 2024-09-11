"""Списки данных для различных запросов"""

headers_base = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.mvideo.ru/',
    'Origin': 'https://www.mvideo.ru',
}


# https://www.mvideo.ru/bff/region/getShops  +
cookies_branches = {
    "MVID_CITY_ID": "CityCZ_6276",
    "MVID_REGION_ID": "17",
    "MVID_REGION_SHOP": "S930",
}

cookies_count_product = {
    'MVID_CITY_ID': 'CityCZ_2534',
    'MVID_REGION_ID': '10',
    'MVID_REGION_SHOP': 'S906',
    'MVID_TIMEZONE_OFFSET': '5',
}



# https://www.mvideo.ru/bff/region/getShops  +
url_list = {
   '' : '',
    '': '',
    '': '',
}





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