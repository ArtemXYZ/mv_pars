"""
    Исследование нового ендпоинта Мвидео на предоставление каталога товаров (по конкретному филиалу)/
    Для подставляемой категории возвращается json, где в print(f'{json_python['body']['categories']}')
    содержатся все необходимые данные, в том числе и для подкатегорий (иерархия). При чем, для иерархии тоже имеются
    данные по количеству товара.
    &offset=0&limit=1' - ни на что не влияют, но должны присутствовать в запросе.

"""

import re
import xmltodict

# from tqdm import tqdm
from parser_03_vers.service_tools import *
# # from parser_03_vers.parsing_patterns import ServiceTools
# from parser_03_vers.service_tools import ServiceTools
# # BaseProperty ParsTools
from requests import Session
from parser_03_vers.params_bank import *

# =========================================================== #  тест
class UrlTest:

    __session: Session = requests.Session()  # Экземпляр сессии:
    __base_headers = BASE_HEADERS

    def __init__(self):
        pass


    def get_response_json__(
            self, url: str = None, params: dict = None, cookies: dict = None, mode: str='json'
            # todo  stream=True) - добавить параметр для больших ответов  \
            #  https://stackoverflow.com/questions/18308529/python-requests-package-handling-xml-response.
    ) -> object | dict | bytes | str:
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
                    data: dict = response.json()  # Ответ в формате JSON
                elif mode == 'text':
                    data: str = response.text
                elif mode == 'bytes':
                    data: bytes = response.content
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
    def pars_sitemap_xml(xml_data: bytes) -> [str, ...]:
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
            Логика: получаем ссылки все с содержанием категорий. Через регулярное выражение отбираем вхождения цифр
            (id категорий), при этом отфильтровываем ссылки с содержанием категорий по установке (они не дают результат,
            мусорные). Далее после получения результатов у нас имеется список с дубликатами категорий, тк в каждой
            ссылке дублируются главная категория и подкатегории. Что бы устранить дубликаты, добавляем этот список
            в сет с результатами, происходит удаление дубликатов.

        """

        results: set = set()
        # Ссылки попавшие под фильтрацию:
        filter_out: set = set()

        # Паттерны регулярных выражений для поиска подстроки в ссылках.

        # Ищет цифры, начинающиеся с дефиса, отбирает только цифры, игнорируя дефис в результате поиска:
        # + проверяет, что за числом следует либо символ /, либо конец строки и игнорирует такие вхождения.
        main_pattern = re.compile(r'(?<!-)-(\d+)(?=/|$)')  # r'\d+'  # r'(?<!-)-\d+' # r'(?<!-)-(\d+)'
        # Ищет вхождения со словом "ustanovka":
        sub_pattern = re.compile(r'\bustanovka\b')

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
                if sub_pattern.search(data_row):
                    filter_out.update(data_row)  # Устарело, заменяем на сеты  append(data_row)
                    # print('Пропуск ссылки с содержанием категории ("ustanovka") ')
                    continue

                # Парсим все айди в урл строке:
                # id_list = re.findall(r'\d+', data_row) # Устарело, замена на более производительное (ниже).
                # Использование re.compile имеет смысл в случаях многократно использования одно и то же рег-выражения:
                id_list: list = main_pattern.findall(data_row)
                # print(id_list)

                # results_temp: set = results_temp + id_list # Устарело, замена на более производительный set.
                results.update(id_list)

        # print(f'Ссылки попавшие под фильтрацию: {filter_out}')

        return list(results)

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


    def recursion_by_json(
            self,
            main_id: str | None,
            parent_id: str | None,
            categories_data: list,
            completed_categories: set,
            result_data_set: list | None = None,


    ) -> None:  # list[dict, ...]
        """

            :param completed_categories:
            :type completed_categories:
            :param main_id:
            :type main_id:
            :param result_data_set:
            :type result_data_set:
            :param categories_data: Передаем список для наполнения результатов.
            :type categories_data: list | None
            :param parent_id: Родительский айди, передаем в рекурсию тоже.
            :type parent_id: str | None.
            :return:
            :rtype:
        """

        if not isinstance(categories_data, list):
            raise TypeError(f'Ошибка, недопустимый тип данных для аргумента "categories_data": '
                            f'{type(categories_data)}. Должен быть "list".')

        if not categories_data:
            raise ValueError(f'Ошибка, данные по категориям отсутствуют, значение:  {categories_data}.')

        try:
            # -----------------------------------------
            category_dict: dict = categories_data[0]
            # ***
            category_id: str = category_dict['id']
            sku_count: str = category_dict['count']
            category_name: str = category_dict['name']
            # ***
            children: list = category_dict['children']
            # -----------------------------------------
        except Exception as error:
            raise ValueError(f'Ошибка доступа к значениям по индексу при обработке данных по категориям: {error}')

        # Создаем словарь с результатами по категории.
        data_set_row = {
            # *** Доп информацйя для создания карты категорий.
            'main_id': main_id,
            'parent_id': parent_id,
            # *** Основная информация.
            'category_id': category_id,
            'sku_count': sku_count,
            'category_name': category_name,
        }

        # Сохраняем наработки в общий список:
        result_data_set.append(data_set_row)

        # Добавляем 'id' категории в set отработанных.
        completed_categories.add(category_id)  # set ? set

        print(f'data_set_row: {data_set_row}')

        # Если есть дочерние элементы (подкатегории), то рекурсия:
        # (Если нет дочерних элементов, children == [])
        if children:

            # print(f'Обработка вложенных категорий для main_id: {main_id}, id: {category_id}')
            # Рекурсия:
            self.recursion_by_json(
                main_id=main_id,
                # Если есть наследники передаем id верхнего уровня (по умолчанию None для главных категорий):
                parent_id=category_id,
                categories_data=children,
                completed_categories=completed_categories,
                result_data_set=result_data_set
            )



    # @staticmethod
    # def search_ids_in_list(search_id: str, array_list: list) -> bool:
    #     """
    #         Поиск id в массиве, если есть - True и наоборот.
    #
    #         :param search_id: Искомый id.
    #         :type search_id: str.
    #         :param array_list: Список для отработанных категорий.
    #         :type array_list: list.
    #         :return: bool.
    #         :rtype: bool.
    #     """
    #
    #     for next_id in array_list:
    #         if next_id == search_id:
    #             return True
    #     else:
    #         return False



    def run(self):
        """
            Цикл итераций по одному филиалу.
        """

        # Список ошибок
        bug_list = []
        # Итоговый список
        result_data_set: list = []

        # Список для отработанных категорий, что бы не повторяться по уже добытым данным.
        # В этот список попадают категории уже извлеченные для итогового дата-сета \
        # (в одном ответе имеется вся структура подкатегорий и главных категорий):
        # P.S. По result_data_set сложнее итерировать (внутри словари, сложнее доставать и сортировать id).
        completed_categories: set = set()   # : list = []

        url_sitemap = 'https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml'

        # Получаем ответ в виде байтов:
        _xml_byte_data: bytes = self.get_response_json__(url_sitemap, mode='bytes')  # text / bytes

        # Получаем все категории (categories_ids) с сайт-мап, [str, ...]:
        _ids = self.pars_sitemap_xml(_xml_byte_data)

        # Перебираем все категории [str, ...]:
        for _id in _ids:

            # time.sleep(3)

            # Проверка: отработана ли данная категория уже:
            if _id in completed_categories:    # completed_categories: set

                print(f'Пропуск категории id: {_id}, completed_categories: {completed_categories}')
                # Если категория уже была обработана, пропускаем ее.
                continue


            # Для каждого _id получаем ответ с сервера МВидео:
            _json = self.count_product_request__(
                # Бузулук, ул. Комсомольская, д. 81, ТРЦ «Север»
                category_id=_id,  #
                id_branch='S659',
                city_id='CityDE_31010',
                region_id='4',
                region_shop_id='S972',
                timezone_offset='4'
            )

            # Обращаемся к нужному контейнеру (отсекаем не нужное):
            # Получаем [{'id': '23715', count': 0, 'name': 'Батуты', 'children': [аналогичная структура], {...}}]
            # categories_data = _json['body']['categories']
            # ------------------------------- alternative
            json_body_data = _json.get('body')
            categories_data = json_body_data.get('categories')

            # Извлекаем информацию о главной категории:
            # В структуре ответа будет всегда первым словарем по порядку, несмотря на выбранную категорию:
            # 'categories': [{'id': '31018', ...}].
            # main_id = categories_data[0]['id']
            # ------------------------------- alternative
            if categories_data:

                first_dict_in_categories_data = categories_data[0]
                main_id = first_dict_in_categories_data.get('id')

                # print(f'Начало обработки категории id: {_id}.')
                # Обходим рекурсивно все вложенные структуры и отдаем список данных. Получаем:
                # [{'main_id': '31018', 'parent_id': '23715', 'id': '23715', count': 0, 'name': 'Батуты', {...}]
                self.recursion_by_json(  # result_data_set =
                    main_id=main_id,
                    parent_id=None,
                    categories_data=categories_data,
                    completed_categories=completed_categories,
                    result_data_set=result_data_set
                )
                print(f'Иог обработки категории id: {_id}:')

            else:
                bug_list.append(json_body_data)
                print(f'bug_list: {bug_list}')

            # break

        return result_data_set


# =========================================================================


q = UrlTest()
# url_sitemap = 'https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml'
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


json_python = q.run()
print(json_python)

# Структура:
# Айди категории: json_python['body']['products']['categories']['id']
