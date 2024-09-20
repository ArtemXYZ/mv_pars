# import requests
# # from bs4 import BeautifulSoup
#
# # Создаём сессию
# session = requests.Session()
# # ----------------------------------------------------------------------------------------------------------------------
# # Запрос на коды магазинов и адреса. Необходимо передать куки.
# url = "https://www.mvideo.ru/bff/region/getShops"
#
# # ----------------------------------------------------------------------------------------------------------------------
# # Заголовки, включая User-Agent и куки
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
#     'Accept': 'application/json',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Referer': 'https://www.mvideo.ru/',
#     'Origin': 'https://www.mvideo.ru',
# }
#
# cookies = {
#     'MVID_CITY_ID': 'CityCZ_6276',
#     'MVID_REGION_ID': '17',
#     'MVID_REGION_SHOP': 'S930',
#     'MVID_CITY_CHANGED': 'true'
# }
# # ----------------------------------------------------------------------------------------------------------------------
# # ----------------------------------------------------------------------------------------------------------------------
# # Первоначальный запрос для захвата всех необходимых куков
# initial_response = session.get('https://www.mvideo.ru/', headers=headers)
#
# # Добавляем куки вручную после начального запроса
# # session.cookies.set('MVID_CITY_ID', 'CityCZ_6276')
# # session.cookies.set('MVID_REGION_ID', '17')
# # session.cookies.set('MVID_REGION_SHOP', 'S930')
# # session.cookies.set('MVID_CITY_CHANGED', 'true')
#
# session.cookies.update(cookies)
#
# # Основной запрос:
# # ----------------------------------------------------------------------------------------------------------------------
#
#
#
# # Выполняем GET-запрос с передачей заголовков и cookies
# response = session.get(url, headers=headers)
#
#
#
#
#
# if response.status_code == 200:
#     data = response.json()
#     print(f'{data}')
# else:
#     print(f"Ошибка: {response.status_code}")
#
#
# # Получаем список names
# # names = data['body']['lemme'][0]['names']
# # print(names)