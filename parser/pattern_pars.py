import requests
# from bs4 import BeautifulSoup

# Создаём сессию
session = requests.Session()
# ----------------------------------------------------------------------------------------------------------------------

# url = 'https://www.mvideo.ru/bff/seo/plp/category-namings/'

# url = 'https://www.mvideo.ru/bff/seo/plp/category-namings?categoryId=205'

# Запрос на коды магазинов и адреса. Необходимо передать куки.
url = "https://www.mvideo.ru/bff/region/getShops"


# ----------------------------------------------------------------------------------------------------------------------
# params = {
#     'categoryId': '205'
# }

# headers = {
#     'Accept': 'application/json',
#     'Accept-Encoding': 'gzip, deflate, br, zstd',
#     'Accept-Language': 'ru,en;q=0.9',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 YaBrowser/24.7.0.0 Safari/537.36',
#     'Referer': 'https://www.mvideo.ru/smartfony-i-svyaz-10/smartfony-205/f/collection_top=skladnye',
#     'Sec-Fetch-Dest': 'empty',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Site': 'same-origin',
#     'X-Set-Application-Id': 'ceb63f68-edd1-43f4-b8d9-d8091facec2e',
# }

# Заголовки, включая User-Agent и куки
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Referer': 'https://www.mvideo.ru/',
    'Origin': 'https://www.mvideo.ru',
}

# Cookies, которые мы передаем в запрос (пример)
cookies = {
    "MVID_CITY_ID": "CityCZ_6276",
    "MVID_REGION_ID": "17",
    # другие cookies, которые могут быть необходимы
    "MVID_REGION_SHOP": "S930",
    "MVID_CITY_CHANGED": "true"
}

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

# response = requests.get(url, params=params)

# Первоначальный запрос для захвата всех необходимых куков
initial_response = session.get('https://www.mvideo.ru/', headers=headers)

# # Если требуется, можно добавить куки вручную после начального запроса
session.cookies.set('MVID_CITY_ID', 'CityCZ_6276')
session.cookies.set('MVID_REGION_ID', '17')
session.cookies.set('MVID_REGION_SHOP', 'S930')
session.cookies.set('MVID_CITY_CHANGED', 'true')

# response = requests.get(url, headers=headers)


# Основной запрос:
# ----------------------------------------------------------------------------------------------------------------------
# Выполняем основной запрос с захваченными куками
response = session.get(url, headers=headers)


# Выполняем GET-запрос с передачей заголовков и cookies
# response = session.get(url, headers=headers, cookies=cookies)

if response.status_code == 200:
    # data = response.text
    data = response.json()
    print(f'{data}')
else:
    print(f"Ошибка: {response.status_code}")


# Получаем список names
# names = data['body']['lemme'][0]['names']
# print(names)