"""
    Исследование нового ендпоинта Мвидео на предоставление каталога товаров (по конкретному филиалу)/
    Для подставляемой категории возвращается json, где в print(f'{json_python['body']['categories']}')
    содержатся все необходимые данные, в том числе и для подкатегорий (иерархия). При чем, для иерархии тоже имеются
    данные по количеству товара.
    &offset=0&limit=1' - ни на что не влияют, но должны присутствовать в запросе.

"""

import re
import xmltodict

from tqdm import tqdm
from parser_03_vers.service_tools import *
# from parser_03_vers.parsing_patterns import ServiceTools
from parser_03_vers.service_tools import ServiceTools
# BaseProperty ParsTools
from requests import Session
from parser_03_vers.params_bank import *

# =========================================================== #  тест
class UrlTest:

    __session: Session = requests.Session()  # Экземпляр сессии:
    __base_headers = BASE_HEADERS

    def get_response_json__(
            self, url: str = None, params: dict = None, cookies: dict = None, mode: str='json'
            # todo  stream=True) - добавить параметр для больших ответов  \
            #  https://stackoverflow.com/questions/18308529/python-requests-package-handling-xml-response.
    ) -> object | bytes | str | any:
        """
            Функция для запросов с мутабельными параметрами.

        """

        # Устанавливаем куки в сессии (если были переданы):
        if cookies:
            self.__session.cookies.update(cookies)

        try:
            # Выполнение запроса с сессией
            response = self.__session.get(url=url, headers=self.__base_headers, params=params)
            # Проверка кода ответа
            if response.status_code == 200:
                if mode == 'json':
                    data = response.json()  # Ответ в формате JSON
                elif mode == 'text':
                    data = response.text
                elif mode == 'bytes':
                    data = response.content
                else:
                    raise ValueError(f'Ошибка параметра "mode": полученное значение {mode} не валидно.'
                                     f'Допустимый синтаксис: "json" (по умолчанию), "text", "bytes".')
            else:
                # Обработка некорректных HTTP ответов
                raise requests.exceptions.HTTPError(f"Ошибка HTTP: {response.status_code} - {response.text}")

        # Перехватываем любые ошибки, включая сетевые и прочие исключения
        except Exception as error_connect:
            raise  # Передача исключения на верхний уровень для обработки
        return data

    @staticmethod
    def pars_sitemap_xml(xml_data: bytes):
        """
            Вспомогательный метод для обработки данных из xml.

            Внутри используется преобразование xml в словарь с вложенными словарями.
                example = {
                    'urlset':
                        {
                            '@xmlns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
                            '@xmlns:news': 'http://www.google.com/schemas/sitemap-news/0.9',
                            '@xmlns:xhtml': 'http://www.w3.org/1999/xhtml',
                            '@xmlns:image': 'http://www.google.com/schemas/sitemap-image/1.1',
                            '@xmlns:video': 'http://www.google.com/schemas/sitemap-video/1.1',

                            'url': [
                                {
                                    'loc': 'https://www.mvideo.ru/sadovaya-tehnika-i-oborudovanie-8027/sadovye-\
                                        telezhki-33570',
                                    'lastmod': '2025-02-07', 'changefreq': 'daily', 'priority': '0.5'
                                },
                                {
                                    'loc': 'https://www.mvideo.ru/sadovaya-tehnika-i-oborudovanie-8027/\
                                        sadovyi-dekor-33716',
                                    'lastmod': '2025-02-07', 'changefreq': 'daily', 'priority': '0.5'
                                },
                            ]
                        }

        """

        results = []

        # Преобразование XML в словарь
        xml_content = xmltodict.parse(xml_data)

        try:
            # Извлекаем основной контейнер с информацией:
            data_list_dict: list[dict,...] = xml_content['urlset']['url']

        except KeyError as e:
            raise ValueError(
                f'Ошибка извлечения данных при попытке обращении к ключам (dict / list) '
                f'преобразованного xml (Lib: "xmltodict") {e}'
            )

        for data_dict in data_list_dict:

            data_row = data_dict.get('loc')

            if data_row:

                # Парсим все айди в урл строке:
                id_list = re.findall(r'\d+', data_row)

                results = results + id_list

        return results

    @staticmethod
    def encoded_request_input_params__(branch_code: str, region_shop_code: str):
        """
         Формирует закодированные параметры запроса для фильтрации.

        :param branch_code: Код филиала
        :param region_shop_code: Код магазина региона
        :return: Список закодированных параметров фильтра
        :rtype: list

        region_shop_code = 'S906'
        branch_code = 'A311'
        """

        results_keys_value = []

        # 1. Формирование фильтров:
        filter_param_9 = f'["Только в наличии","-9","Да"]'
        filter_param_12 = f'["Забрать из магазина по адресу","-12","{branch_code}"]'
        filter_param_11 = f'["Забрать через 15 минут","-11","{region_shop_code}"]'
        filter_tuple = (filter_param_9, filter_param_12, filter_param_11)

        # 2. Кодирование:
        for param_list in filter_tuple:
            # Преобразование списка в строку
            joined_string = str(param_list)

            encoded_list = joined_string.encode('utf-8')  # Преобразуем списки в строку и кодируем в  в байты 'utf-8':
            base64_encoded = base64.b64encode(encoded_list).decode('utf-8')  # Base64-кодирование
            # print(f"Base64-кодированная строка: {base64_encoded}")
            final_encoded = urllib.parse.quote(base64_encoded)  # URL-кодирование
            # print(f"Итоговый URL-кодированный параметр: {final_encoded}")

            # 3. Сохраняем в виде словаря для передачи как параметр в строку запроса.
            # Добавляем в список результат кодирования:
            results_keys_value.append(final_encoded)  # Ожидаем на выход: [рез1, рез2, рез3]
            # print(results_keys_value)

        filter_params = (f'&filterParams={results_keys_value[0]}'
                         f'&filterParams={results_keys_value[1]}'
                         f'&filterParams={results_keys_value[2]}')

        return filter_params

    def count_product_request__(self, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset,
                                url=None
                                ):
        """
        # ---------------- Расшифрованные filterParams:
        # 1. ["Только в наличии","-9","Да"] = 'WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'
        # 2. ["Забрать из магазина по адресу","-12","S668"] =  \
        WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjY4Il0%3D
        # 3. '["Забрать через 15 минут","-11","S972"]' = \
        WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D
        """



        # Формирование закодированных параметров фильтрации в запросе:
        result_filters_params = self.encoded_request_input_params__(id_branch, region_shop_id)

        # --------------------------------------- Переменные:
        # Базовая строка подключения:
        # url_count_old = f'https://www.mvideo.ru/bff/products/listing?categoryId={category_id}&offset=0&limit=1'
        url_count = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0&limit=1'

        if url:
            url_count = url

        # categoryId - обязательно

        # Конструктор куков:
        cookies_count_product = {
            'MVID_CITY_ID': city_id,
            'MVID_REGION_ID': region_id,
            'MVID_REGION_SHOP': region_shop_id,
            'MVID_TIMEZONE_OFFSET': timezone_offset,
        }

        # Полная строка с фильтрами:
        full_url = f'{url_count}{result_filters_params}'
        # ---------------------------------------
        # ---------------------------------------- Выполняем основной запрос:
        # Запрос на извлечение count_product (на вход бязательны: \
        # MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET):
        data = self.get_response_json__(url=full_url, cookies=cookies_count_product)
        return data


    def recursion_json(self, data: list):
        # if isinstance(structure, dict):

        if data:
            data_set_raw = data
        else:
            data_set_raw = []
        # -----------------------------------------

        # 'categories': [{}] 1
        for key, value in data[0].items():
            row_dict = {}
            # Добавляем данные в новый словарь:
            if key == 'id':
                row_dict[key] = value

            elif key == 'count':
                row_dict[key] = value

            elif key == 'name':
                row_dict[key] = value

            # Всегда содержит []
            elif key == 'children':
                # Сохраняем наработки в общий список:
                data_set_raw.append(row_dict)

                # Если список не пустой - есть дочерние элементы:
                if value:
                    # Рекурсия:
                    self.recursion_json(data_set_raw)

            # todo родумать, как вытаскивать перент айди

            # id = 'id'
            # count =
            # name =
            # children =



    def run(self):
        """


        """


        url_sitemap = 'https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml'

        # Получаем ответ в виде байтов:
        _xml_byte_data: bytes = self.get_response_json__(url_sitemap, mode='bytes')  # text / bytes

        # categories_ids
        _ids = self.pars_sitemap_xml(_xml_byte_data)

        for _id in _ids:

            _json = q.count_product_request__(
                # Бузулук, ул. Комсомольская, д. 81, ТРЦ «Север»
                category_id=_id,  #
                id_branch='S659',
                city_id='CityDE_31010',
                region_id='4',
                region_shop_id='S972',
                timezone_offset='4'
            )

            d = _json['body']['categories']['id']


# =========================================================================


# q = UrlTest()
# result_xml = q.get_response_json__(url_sitemap, mode='bytes')  # data = response.text bytes
# # print(f'result_xml: {result_xml}')
#
# w = q.pars_sitemap_xml(result_xml)
# print(f'Итог: {w}')



# json_python = q.count_product_request__(
#     # Бузулук, ул. Комсомольская, д. 81, ТРЦ «Север»
#     category_id='133',  #
#     id_branch='S659',
#     city_id='CityDE_31010',
#     region_id='4',
#     region_shop_id='S972',
#     timezone_offset='4'
# )
#


# print(json_python)

# Структура:
# Айди категории: json_python['body']['products']['categories']['id']





