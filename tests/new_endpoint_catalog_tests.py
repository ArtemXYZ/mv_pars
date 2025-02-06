"""
    Исследование нового ендпоинта Мвидео на предоставление каталога товаров (по конкретному филиалу)/
    Для подставляемой категории возвращается json, где в print(f'{json_python['body']['categories']}')
    содержатся все необходимые данные, в том числе и для подкатегорий (иерархия). При чем, для иерархии тоже имеются
    данные по количеству товара.
    &offset=0&limit=1' - ни на что не влияют, но должны присутствовать в запросе.

"""
from xml.etree import ElementTree as ET
from tqdm import tqdm
from parser_03_vers.service_tools import *
# from parser_03_vers.parsing_patterns import ServiceTools
from parser_03_vers.service_tools import ServiceTools
# BaseProperty ParsTools
from requests import Session
from parser_03_vers.params_bank import *


def _base64_decoded(url_param_string):
    """
        Расшифровка параметров URL.
        :param url_param_string: (base64_string)
        :type url_param_string:
        :return:
        :rtype:
    """
    try:
        # Шаг 1: URL-декодирование
        url_param_string_decoded = urllib.parse.unquote(url_param_string)
        # Шаг 2: Base64-декодирование
        base64_decoded_string = base64.b64decode(url_param_string_decoded).decode('utf-8')
        return base64_decoded_string
    except Exception as e:
        print(f'Ошибка декодирования: {e}')
        return None


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

# category_id = 205
# MVID_CITY_ID, MVID_REGION_ID, MVID_REGION_SHOP, MVID_TIMEZONE_OFFSET
# url_new_construct = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0'

# ендпоинт.
url_new = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds=205&offset=0'

url_new_all_params = 'https://www.mvideo.ru/bff/products/v2/search?categoryIds=205&offset=0&filterParams=WyLQotC%2B0LvRjNC60L4g0L\
Ig0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiL\
CItMTEiLCJTOTcyIl0%3D&filterParams=WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMT\
IiLCJTNjU5Il0%3D&doTranslit=false&limit=48&context=v2dzaG9wX2lkZFM5NzJsY2F0ZWdvcnlfaWRzn2MyMDX%2FZmNhdF9JZGMyMDX%2F'

# Значение переменной: ["Только в наличии","-9","Да"]
url_new_params_1 = 'WyLQotC%2B0LvRjNC60L4g0LIg0L3QsNC70LjRh9C40LgiLCItOSIsItCU0LAiXQ%3D%3D'

# filterParams: ["Забрать через 15 минут","-11","S972"]
url_new_params_2 = 'WyLQl9Cw0LHRgNCw0YLRjCDRh9C10YDQtdC3IDE1INC80LjQvdGD0YIiLCItMTEiLCJTOTcyIl0%3D'

# filterParams: ["Забрать из магазина по адресу","-12","S659"]
url_new_params_3 = (f'WyLQl9Cw0LHRgNCw0YLRjCDQuNC3INC80LDQs9Cw0LfQuNC90'
                    f'LAg0L%2FQviDQsNC00YDQtdGB0YMiLCItMTIiLCJTNjU5Il0%3D')

url_new_params_4 = 'doTranslit=false'
url_new_params_5 = 'limit=48'

# &context= : Ошибка декодирования: 'utf-8' codec can't decode byte 0xbf in position 0: invalid start byte
url_new_params_6 = 'v2dzaG9wX2lkZFM5NzJsY2F0ZWdvcnlfaWRzn2MyMDX%2FZmNhdF9JZGMyMDX%2F'


# не разобрано.
cookie = ('MVID_NEW_LK_OTP_TIMER=true; mindboxDeviceUUID=aad4557b-4cd3-4e9a-92d7-70b036354920;'
          ' directCrm-session=%7B%22deviceGuid%22%3A%22aad4557b-4cd3-4e9a-92d7-70b036354920%22%7D;'
          ' _ym_uid=1704964204828610292; _ga=GA1.1.964250854.1704964204; MVID_GUEST_ID=23429757235;'
          ' searchType2=1; MVID_NEW_OLD=eyJjYXJ0IjpmYWxzZSwiZmF2b3JpdGUiOnRydWUsImNvbXBhcmlzb24iOnRydWV9;'
          ' MVID_OLD_NEW=eyJjb21wYXJpc29uIjogdHJ1ZSwgImZhdm9yaXRlIjogdHJ1ZSwgImNhcnQiOiB0cnVlfQ==;'
          ' tmr_lvid=a42c61717f67735237edcdae5c08dc3e; tmr_lvidTS=1704964209111; adrcid=A4koYzdJrqryE98X2z-mntg;'
          ' afUserId=46c7e94c-1537-4ba2-b0c9-10e916410d6e-p; uxs_uid=3a0d71e0-b061-11ee-928d-27da829e2648;'
          ' MVID_CHAT_VERSION=6.6.0; SENTRY_TRANSACTIONS_RATE=0.1; SENTRY_REPLAYS_SESSIONS_RATE=0.01;'
          ' SENTRY_REPLAYS_ERRORS_RATE=0.01; SENTRY_ERRORS_RATE=0.1; MVID_FILTER_CODES=true;'
          ' MVID_FLOCKTORY_ON=true; MVID_CRITICAL_GTM_INIT_DELAY=3000; MVID_SP=true;'
          ' MVID_DIGINETICA_ENABLED=true; _userGUID=0:m0uj1o7i:xV22WXCjACRtXaKuFFqDdZifG66Qpibm;'
          ' _ym_d=1725857613; gdeslon.ru.__arc_domain=gdeslon.ru; '
          'gdeslon.ru.user_id=7c0aa005-0048-4363-a62f-234ed414d5f6; '
          'adrcid=A4koYzdJrqryE98X2z-mntg; MVID_GEOLOCATION_NEEDED=false; '
          '__USER_ID_COOKIE_NAME__=172683185362879; MVID_TIMEZONE_OFFSET=4;'
          ' MVID_REGION_ID=4; MVID_REGION_SHOP=S972; MVID_CITY_ID=CityCZ_3798;'
          ' MVID_KLADR_ID=6300000600000; MVID_SERVICES=111;'
          ' MVID_NEW_LK_CHECK_CAPTCHA=true; MVID_GTM_ENABLED=011; '
          'MVID_EMPLOYEE_DISCOUNT=true; __SourceTracker=yandex.ru__organic;'
          ' admitad_deduplication_cookie=yandex.ru__organic; MVID_MEDIA_STORIES=true;'
          ' MVID_SERVICE_AVLB=true; MVID_MCOMBO_SUBSCRIPTION=true;'
          ' MVID_WEB_QR=true; __lhash_=2c1fe3e4b1792a3cef4a5e5727d7d0f4;'
          ' MVID_SUGGEST_DIGINETICA=true; MVID_IS_NEW_BR_WIDGET=true; '
          'MVID_WEB_SBP=true; MVID_CREDIT_SERVICES=true; MVID_TYP_CHAT=true; '
          'MVID_CREDIT_DIGITAL=true; MVID_CASCADE_CMN=true; MVID_AB_UPSALE=true;'
          ' MVID_AB_PERSONAL_RECOMMENDS=true; MVID_ACCESSORIES_PDP_BY_RANK=true;'
          ' MVID_NEW_CHAT_PDP=true; MVID_GROUP_BY_QUALITY=true; '
          'MVID_DISPLAY_PERS_DISCOUNT=true; MVID_AB_PERSONAL_RECOMMENDS_SRP=true;'
          ' MVID_ACCESSORIES_ORDER_SET_VERSION=2; MVID_BYPASS_FC=true;'
          ' MVID_IMG_RESIZE=true; MVID_NEW_GET_SHOPPING_CART=true; '
          'MVID_NEW_GET_SHOPPING_CART_SHORT=true; MVID_MCOMBO_HISTORY=true;'
          ' MVID_SRP_SEARCH_V3=true; MVID_PLP_SEARCH_V3=true;'
          ' MVID_ALLPROMOTIONS_NEW=true; MVID_SORM_INTEGRATION=true;'
          ' MVID_DISABLEDITEM_PRICE=1; MVID_RECOMENDATION_SET_ALGORITHM=1;'
          ' MVID_ENVCLOUD=prod1; _ym_isad=2; _sp_ses.d61c=*; SMSError=;'
          ' authError=; advcake_track_id=69fdfd03-ae86-5f79-7959-e6564d3667b7; '
          'advcake_session_id=36f0b0bd-57b4-0101-0dac-330e4d0e4cee; '
          'acs_3=%7B%22hash%22%3A%22efc4edc6204628178e8c6c2658f73159fe6d444f%22%2C%22nextSyncTime%22%3A1738310527009\
          %2C%22syncLog%22%3A%7B%22224%22%3A1738224127009%2C%221228%22%3A1738224127009%7D%7D; '
          'acs_3=%7B%22hash%22%3A%22efc4edc6204628178e8c6c2658f73159fe6d444f%22%2C%22nextSyncTime%22%3A1738310\
          527009%2C%22syncLog%22%3A%7B%22224%22%3A1738224127009%2C%221228%22%3A1738224127009%7D%7D; '
          'adrdel=1738224127275; adrdel=1738224127275; AF_SYNC=1738224127475; '
          'flocktory-uuid=2a435f39-6a4e-4b8f-a078-03f1d765cced-0; flacktory=no;'
          ' BIGipServeratg-ps-prod_tcp80=2969885706.20480.0000; '
          'bIPs=-971835924; domain_sid=-nijVdXbCI2zLlmLD1Ela%3A1738224128698;'
          ' digi_uc=|v:172899:4154603:400011614:400270562:4099435:400040071:400059466:400378229!172906:40036089\
          2!173017:30070141!173218:400340563|c:172899:4154583:400011614!172906:20074441!173017:400256\
          342!173822:30074323; adid=173822521102047; __hash_=f2907ea822bce0224786d48c0356aebb;'
          ' dSesn=4c1564de-3d3d-65e3-643c-4623806df50c; _dvs=0:m6j4i7tc:IOZRqgumoYCmZnpvUT9zEZYlJStn4l0c;'
          ' _ym_visorc=w; MVID_VIEWED_PRODUCTS=; wurfl_device_id=generic_web_browser; '
          'JSESSIONID=D7RBnbHBFvbG82lGQLyRnnJTLhQ7yply0FCTTbwXd7Ww1VSlrpK1!-1345026164; '
          'COMPARISON_INDICATOR=false; BIGipServeratg-ps-prod_tcp80_clone=2969885706.20480.0000; '
          'MVID_GTM_BROWSER_THEME=1; CACHE_INDICATOR=false; deviceType=desktop;'
          'advcake_track_url=%3D20250113Yz9N7CE5jsFbdzSqk8fcG4bn%2Fvc8cEsTm1nfPLs8OiFJYjUUaf%2BnFFbGcKOVv5jskberpQK\
          iDIytNdN9wtRu7spSgkh33YSV6FeUJyxy%2F7bhI5OnSweR3EEy7wfQIBt1TyAMNJIMmqu5ySXGuNfBsOPQ6lpoyyTBIgivkNT\
          UAZwdpw2ZvwMSuYLvNETDU6zemz52ApWIKW1rjjzMhtXISzjfLFliivxF9y%2F%2BWwNfKopHVZAstOkUV%2F0G0mGm3Ff%2Fcb\
          CbIekMwAQBpQBNLbaTVmlPmsjMZqUagOkZ4l0vw2XniaxAIRndlfPiAKFj50Q%2FKklqrKnu7R9wDGrlUvBHgs5hLYNnA%2Bdg\
          ex5QLEB6xwMJnxSlynfnF3xc83S5AjvCboN2LghFfW%2BglQxbE%2BADPajXL6ax7okf8Deis7MTI9TaTaoETnm%2BNWiy6vtxL\
          9J9e9BgA%2BQSRq2Ewtep%2FkndMTqC8CvevwJfaCXhC7%2FEt6NRq4zBKJNelmdD1xV3iYlkg%2FXQfAXBbkbQbzfcTCizQ%2\
          Bxw72Oiy06BiKCA%2FVTPMz5OLYZWvEEVA%2FR7%2BZayZh8pjVX9D8Hv6JYV%2BOYL968n6R%2B%2B6s55tjR8Le7FuxN319ZYS\
          huqIV6G6iHYHmwbS9PzFI08hkB0oAAeABWVAfEs1kHilwrGo7q%2B6Q5dKvM%2Bezd7tUwlyw42voU%3D; '
          'tmr_detect=0%7C1738229632787; '
          '_ga_CFMZTSS5FM=GS1.1.1738228724.60.1.1738229659.0.0.0; _ga_BNX5WPP3YK=GS1.1.1738228724.60.1.1738229659.3.0.0; gsscgib-w-mvideo=TmdPzdjooV4tvcURiw/kwCfA3ZaLpKp7KGhRGj+Jsl6DiH2CH8rdbPlzeGGthj+JiBTOPsGJJeFWvZLFic4OaUTpOdF5ncZgqodjSUnjMu98i3fehPpGvfLNteN55ZSl2iWMHT70QbpS7OnYZ2f+gzQILLAJxaSp+Eij3T/TtvZx+r8LegiMDhkT3HDlNB3KUiyJ6qAql00X3VZ6p5XJSqmlAcK6irsp9qSvV77h0iJNusceqA8KM+KJyQ3P7ihYvPspO7RKpDT+l7a0z7Z5jw==; cfidsgib-w-mvideo=waJH7MCf76eiFj86uPMu07PwYbGIUDpIN6dE06insSIbzRW9Swehi5z6fDzcx4R9EIO2EeXK7PgQTbkjNTzQpfKaJ5YufFe8aqpZ0dwA6dyPaluYNuKTR8uNw2rQ413IFLyOz/PenkRrnN9103Qg3FNnxWr6BUf+zj8t9DeBsQ==; gsscgib-w-mvideo=TmdPzdjooV4tvcURiw/kwCfA3ZaLpKp7KGhRGj+Jsl6DiH2CH8rdbPlzeGGthj+JiBTOPsGJJeFWvZLFic4OaUTpOdF5ncZgqodjSUnjMu98i3fehPpGvfLNteN55ZSl2iWMHT70QbpS7OnYZ2f+gzQILLAJxaSp+Eij3T/TtvZx+r8LegiMDhkT3HDlNB3KUiyJ6qAql00X3VZ6p5XJSqmlAcK6irsp9qSvV77h0iJNusceqA8KM+KJyQ3P7ihYvPspO7RKpDT+l7a0z7Z5jw==; gsscgib-w-mvideo=TmdPzdjooV4tvcURiw/kwCfA3ZaLpKp7KGhRGj+Jsl6DiH2CH8rdbPlzeGGthj+JiBTOPsGJJeFWvZLFic4OaUTpOdF5ncZgqodjSUnjMu98i3fehPpGvfLNteN55ZSl2iWMHT70QbpS7OnYZ2f+gzQILLAJxaSp+Eij3T/TtvZx+r8LegiMDhkT3HDlNB3KUiyJ6qAql00X3VZ6p5XJSqmlAcK6irsp9qSvV77h0iJNusceqA8KM+KJyQ3P7ihYvPspO7RKpDT+l7a0z7Z5jw==; _sp_id.d61c=67bf8e33-50ef-48d1-93a0-d365eb213dc4.1704964204.71.1738229661.1732184618.af11fc47-3169-4e06-b92c-9cf004e504c7.662e5b79-2f96-4e9c-9a26-7c089fa27d10.065cf0b7-7fdb-4163-a1aa-46282da76533.1738224122890.276; fgsscgib-w-mvideo=T2FH0eb667cc634a9b28e2b5f1de2705423fc667; fgsscgib-w-mvideo=T2FH0eb667cc634a9b28e2b5f1de2705423fc667')


# url_new_params_decoded = _base64_decoded(url_new_params_2)
# print(url_new_params_decoded)  # ["Только в наличии","-9","Да"]


# todo: Нужно искать categories! ['body'][categories]
#         "categories": [
#             {
#                 "id": "11",
#                 "count": 3,
#                 "name": "Климатическая техника",
#                 "children": [
#                     {
#                         "id": "161",
#                         "count": 3,
#                         "name": "Метеостанции и термометры",
#                         "children": [
#                             {
#                                 "id": "407",
#                                 "count": 3,
#                                 "name": "Метеостанции",
#                                 "children": [],
#                                 "translitName": "meteostancii",
#                                 "isSeo": true
#                             },
#                             {
#                                 "id": "436",
#                                 "count": 0,
#                                 "name": "Дистанционные датчики",
#                                 "children": [],
#                                 "translitName": "distancionnye-datchiki",
#                                 "isSeo": true
#                             }
#                         ],
#                         "translitName": "meteostancii-i-termometry",
#                         "urlFacetCrossBlock": null
#                     }
#                 ],
#                 "translitName": "klimaticheskaya-tehnika"
# =========================================================== #  тест
#

class UrlTest:

    __session: Session = requests.Session()  # Экземпляр сессии:
    __base_headers = BASE_HEADERS

    def get_response_json__(
            self, url: str = None, params: dict = None, cookies: dict = None, mode: str='json'
    ) -> object:
        """Функция для запросов с мутабельными параметрами. """

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


    # detect_sub_level(xml_array_part, tag_or_substructures: str | list | dict, mode: str):

    def parse_by_tags(self, xml_array, commands_structure: str | list | dict):
        """
            Вспомогательный метод для рекурсивного разбора словаря тегов.

            Базовая структура для распознавания логикой:

                * tag_structure = {
                    'findall': [  # <- or 'find'
                        'url', {'find': 'loc'}
                    ]
                }

                # ['url']['loc']
                tag_structure = [{'findall': 'url'}, {'find': 'loc'}]

                ,где  management_key - ключ дает команду на вызов метода find или findall.

            Логика:
                Проходимся рекурсивно по структуре словаря и в зависимости от ключей управления "management_key"
                вызываем соответствующий метод. Результат сохраняем в список.
        """

        results = []





        # Проверка на пустоту параметров

        # Перебираем рекурсивно все команды управления
        for management_key, tag_or_substructures in commands_structure.items():

            long_substructures = len(tag_or_substructures)

            # 1. ------------------------------- Если необходим поиск всех тегов в xml:
            if management_key == 'findall':

                # Обращаемся к значению, если это просто tag xml (например: 'url'), тогда:
                if isinstance(tag_or_substructures, str):

                    # Используем findall для извлечения всех элементов:
                    elements_data = xml_array.findall(tag_or_substructures)       #

                    # Если это тег (конечная точка, подуровней нет), тогда:
                    if long_substructures == 1:
                        # Добавляем значение в список для результатов:
                        results.append(elements_data.text)
                        break
                    else:
                        self.parse_by_tags(elements_data)

                # Если это список tag xml (например: 'url'), тогда:
                elif isinstance(tag_or_substructures, list):
                    ...


                # Если это список tag xml (например: 'url'), тогда:
                elif isinstance(tag_or_substructures, dict):
                    ...

            # elements_data.


            # 2. ------------------------------- Если необходим поиск только 1-го тега в xml:
            elif management_key == 'find':
               ...


            else:
                raise ValueError(
                    f'Ошибка, недопустимое значения ключа: {management_key} '
                    f'в параметре "commands_structure": {commands_structure}.'
                )


        return results

    # @staticmethod
    # def xml_teg_grabber(self, row_xml: bytes, xml_tags_by_pars: dict):
    #     """
    #         Метод обработки xml файлов.
    #         Принимает xml в байт-формате (data = response.content), разбирает информацию по переданному тегу.
    #     """
    #
    #     key, tags = xml_tags_by_pars.items()
    #
    #
    #     # После преобразования row_xml получаем доступ ко вложенным данным главного контейнера страницы:
    #     xml_data = ET.fromstring(row_xml)
    #
    #     # Итерируем по всем элементам <url> в корневом элементе
    #     for url in xml_data.findall('url'):
    #         loc = url.find('loc').text
    #         lastmod = url.find('lastmod').text
    #         changefreq = url.find('changefreq').text
    #         priority = url.find('priority').text



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




# =========================================================================
# 3.1.1.1) Основной запрос (возвращает json (пайтон)):
q = UrlTest()

json_python = q.count_product_request__(
    # Бузулук, ул. Комсомольская, д. 81, ТРЦ «Север»
    category_id='133',  #
    id_branch='S659',
    city_id='CityDE_31010',
    region_id='4',
    region_shop_id='S972',
    timezone_offset='4'
)

# +
print(f'{json_python['body']['categories']}')

# +
# print(f'selected_categories_ids: {json_python['body']['selected_categories_ids']}')

# print(json_python)

qwerqw = {
    'success': True,
    'messages': [],
    'body': {
        'total': 0,
        'type': 'plain',
        'products': [],
        'filters': [
            {
                'name': 'Бренд',
                'selected': False, 'translitName': 'brand', 'type': 'vendor', 'codes': [-2],
                'criterias': [
                    {'name': 'UNIX line', 'value': 'UNIX line', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'unix-line',
                     'selected': False, 'isSeo': True},
                    {'name': 'Hasttings', 'value': 'Hasttings', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'hasttings',
                     'selected': False, 'isSeo': True},
                    {'name': 'Evo Jump', 'value': 'Evo Jump', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'evo-jump',
                     'selected': False, 'isSeo': True},
                    {'name': 'Wallaby', 'value': 'Wallaby', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'wallaby',
                     'selected': False, 'isSeo': True},
                    {'name': 'Bradex', 'value': 'Bradex', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'bradex',
                     'selected': False, 'isSeo': True},
                    {'name': 'Sport Elite', 'value': 'Sport Elite', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'sport-elite', 'selected': False, 'isSeo': True},
                    {'name': 'ARLAND', 'value': 'ARLAND', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'arland',
                     'selected': False, 'isSeo': True},
                    {'name': 'Dfc', 'value': 'Dfc', 'count': 0, 'translitName': 'vendor', 'translitValue': 'dfc',
                     'selected': False,
                     'isSeo': True},
                    {'name': 'Green Glade', 'value': 'Green Glade', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'green-glade', 'selected': False, 'isSeo': True},
                    {'name': 'ONLITOP', 'value': 'ONLITOP', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'onlitop',
                     'selected': False, 'isSeo': True},
                    {'name': 'ONLYTOP', 'value': 'ONLYTOP', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'onlytop',
                     'selected': False, 'isSeo': True},
                    {'name': 'Yamota\xa0', 'value': 'Yamota\xa0', 'count': 0, 'translitName': 'vendor',
                     'translitValue': 'yamota',
                     'selected': False, 'isSeo': True}
                ],
                'urlFacetCrossBlock': None
            },
            {
                'name': 'Акции',
                'selected': False,
                'translitName': 'akcii',
                'type': 'akcii',
                'codes': [-1],
                'criterias': [
                    {'name': 'Скидки до 30% по промокоду на акционные товары',
                     'value': 'Скидки до 30% по промокоду на акционные товары', 'count': 0, 'translitName': 'akcii',
                     'translitValue': 'skidki-do-30-po-promokodu-na-akcionnye-tovary', 'selected': False, 'isSeo': True}
                ],
                'urlFacetCrossBlock': None
            },
            {
                'name': 'Диаметр', 'selected': False, 'translitName': 'diametr', 'type': 'diametr',
                'codes': [601500, 620175],
                'criterias': [{'name': 'до 100 см', 'value': 'до 100 см', 'count': 0, 'translitName': 'diametr',
                               'translitValue': 'do-100-sm', 'selected': False, 'isSeo': True},
                              {'name': '101 - 150 см', 'value': '101 - 150 см', 'count': 0, 'translitName': 'diametr',
                               'translitValue': '101---150-sm', 'selected': False, 'isSeo': True},
                              {'name': '151 - 200 см', 'value': '151 - 200 см', 'count': 0, 'translitName': 'diametr',
                               'translitValue': '151---200-sm', 'selected': False, 'isSeo': True},
                              {'name': '201 - 300 см', 'value': '201 - 300 см', 'count': 0, 'translitName': 'diametr',
                               'translitValue': '201---300-sm', 'selected': False, 'isSeo': True},
                              {'name': 'более 300 см', 'value': 'более 300 см', 'count': 0, 'translitName': 'diametr',
                               'translitValue': 'bolee-300-sm', 'selected': False, 'isSeo': True}],
                'urlFacetCrossBlock': None
            },
            {'name': 'Максимальная нагрузка', 'selected': False, 'translitName': 'maksimalnaya-nagruzka',
             'type': 'maksimalnaya-nagruzka', 'codes': [11930], 'criterias': [
                {'name': 'до 50 кг', 'value': 'до 50 кг', 'count': 0, 'translitName': 'maksimalnaya-nagruzka',
                 'translitValue': 'do-50-kg', 'selected': False, 'isSeo': True},
                {'name': '51 - 80 кг', 'value': '51 - 80 кг', 'count': 0, 'translitName': 'maksimalnaya-nagruzka',
                 'translitValue': '51---80-kg', 'selected': False, 'isSeo': True},
                {'name': '81 - 100 кг', 'value': '81 - 100 кг', 'count': 0, 'translitName': 'maksimalnaya-nagruzka',
                 'translitValue': '81---100-kg', 'selected': False, 'isSeo': True},
                {'name': '101 - 150 кг', 'value': '101 - 150 кг', 'count': 0, 'translitName': 'maksimalnaya-nagruzka',
                 'translitValue': '101---150-kg', 'selected': False, 'isSeo': True},
                {'name': 'более 150 кг', 'value': 'более 150 кг', 'count': 0, 'translitName': 'maksimalnaya-nagruzka',
                 'translitValue': 'bolee-150-kg', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Защитная сетка', 'selected': False, 'translitName': 'zashhitnaya-setka',
             'type': 'zashhitnaya-setka',
             'codes': [3482], 'criterias': [
                {'name': 'да', 'value': 'да', 'count': 0, 'translitName': 'zashhitnaya-setka', 'translitValue': 'da',
                 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Высота защитной сетки', 'selected': False, 'translitName': 'vysota-zashhitnoi-setki',
             'type': 'vysota-zashhitnoi-setki', 'codes': [30853496], 'criterias': [
                {'name': '101 - 150 см', 'value': '101 - 150 см', 'count': 0, 'translitName': 'vysota-zashhitnoi-setki',
                 'translitValue': '101---150-sm', 'selected': False, 'isSeo': True},
                {'name': '151 - 200 см', 'value': '151 - 200 см', 'count': 0, 'translitName': 'vysota-zashhitnoi-setki',
                 'translitValue': '151---200-sm', 'selected': False, 'isSeo': True},
                {'name': 'более 200 см', 'value': 'более 200 см', 'count': 0, 'translitName': 'vysota-zashhitnoi-setki',
                 'translitValue': 'bolee-200-sm', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Материал корпуса', 'selected': False, 'translitName': 'material-korpusa',
             'type': 'material-korpusa',
             'codes': [83, 4462], 'criterias': [
                {'name': 'металл', 'value': 'металл', 'count': 0, 'translitName': 'material-korpusa',
                 'translitValue': 'metall',
                 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Материал прыжковой части', 'selected': False, 'translitName': 'material-pryzhkovoi-chasti',
             'type': 'material-pryzhkovoi-chasti', 'codes': [30853545], 'criterias': [
                {'name': 'полипропилен', 'value': 'полипропилен', 'count': 0,
                 'translitName': 'material-pryzhkovoi-chasti',
                 'translitValue': 'polipropilen', 'selected': False, 'isSeo': True},
                {'name': 'перматрон', 'value': 'перматрон', 'count': 0, 'translitName': 'material-pryzhkovoi-chasti',
                 'translitValue': 'permatron', 'selected': False, 'isSeo': True},
                {'name': 'ПВХ', 'value': 'ПВХ', 'count': 0, 'translitName': 'material-pryzhkovoi-chasti',
                 'translitValue': 'pvh', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Количество жгутов', 'selected': False, 'translitName': 'kolichestvo-zhgutov',
             'type': 'kolichestvo-zhgutov', 'codes': [30855551], 'criterias': [
                {'name': '48 шт', 'value': '48 шт', 'count': 0, 'translitName': 'kolichestvo-zhgutov',
                 'translitValue': '48-sht', 'selected': False, 'isSeo': True},
                {'name': '60 шт', 'value': '60 шт', 'count': 0, 'translitName': 'kolichestvo-zhgutov',
                 'translitValue': '60-sht', 'selected': False, 'isSeo': True},
                {'name': '36 шт', 'value': '36 шт', 'count': 0, 'translitName': 'kolichestvo-zhgutov',
                 'translitValue': '36-sht', 'selected': False, 'isSeo': True},
                {'name': '72 шт', 'value': '72 шт', 'count': 0, 'translitName': 'kolichestvo-zhgutov',
                 'translitValue': '72-sht', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Длина ножек', 'selected': False, 'translitName': 'dlina-nozhek', 'type': 'dlina-nozhek',
             'codes': [618453], 'criterias': [
                {'name': '38 см', 'value': '38 см', 'count': 0, 'translitName': 'dlina-nozhek',
                 'translitValue': '38-sm',
                 'selected': False, 'isSeo': True},
                {'name': '26 см', 'value': '26 см', 'count': 0, 'translitName': 'dlina-nozhek',
                 'translitValue': '26-sm',
                 'selected': False, 'isSeo': True},
                {'name': '76 см', 'value': '76 см', 'count': 0, 'translitName': 'dlina-nozhek',
                 'translitValue': '76-sm',
                 'selected': False, 'isSeo': True},
                {'name': '86 см', 'value': '86 см', 'count': 0, 'translitName': 'dlina-nozhek',
                 'translitValue': '86-sm',
                 'selected': False, 'isSeo': True},
                {'name': '99 см', 'value': '99 см', 'count': 0, 'translitName': 'dlina-nozhek',
                 'translitValue': '99-sm',
                 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Высота', 'selected': False, 'translitName': 'vysota', 'type': 'vysota', 'codes': [111],
             'criterias': [
                 {'name': 'до 25 см', 'value': 'до 25 см', 'count': 0, 'translitName': 'vysota',
                  'translitValue': 'do-25-sm',
                  'selected': False, 'isSeo': True},
                 {'name': '101 - 200 см', 'value': '101 - 200 см', 'count': 0, 'translitName': 'vysota',
                  'translitValue': '101---200-sm', 'selected': False, 'isSeo': True},
                 {'name': 'более 200 см', 'value': 'более 200 см', 'count': 0, 'translitName': 'vysota',
                  'translitValue': 'bolee-200-sm', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Лестница', 'selected': False, 'translitName': 'lestnica', 'type': 'lestnica', 'codes': [605078],
             'criterias': [
                 {'name': 'да', 'value': 'да', 'count': 0, 'translitName': 'lestnica', 'translitValue': 'da',
                  'selected': False,
                  'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Чехол', 'selected': False, 'translitName': 'chehol', 'type': 'chehol', 'codes': [461],
             'criterias': [
                 {'name': 'Да', 'value': 'Да', 'count': 0, 'translitName': 'chehol', 'translitValue': 'da',
                  'selected': False,
                  'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Вес', 'selected': False, 'translitName': 'ves', 'type': 'ves', 'codes': [91], 'criterias': [
                {'name': 'до 9 кг', 'value': 'до 9 кг', 'count': 0, 'translitName': 'ves', 'translitValue': 'do-9-kg',
                 'selected': False, 'isSeo': True},
                {'name': '16 - 30 кг', 'value': '16 - 30 кг', 'count': 0, 'translitName': 'ves',
                 'translitValue': '16---30-kg',
                 'selected': False, 'isSeo': True},
                {'name': '31 - 51 кг', 'value': '31 - 51 кг', 'count': 0, 'translitName': 'ves',
                 'translitValue': '31---51-kg',
                 'selected': False, 'isSeo': True},
                {'name': 'более 51 кг', 'value': 'более 51 кг', 'count': 0, 'translitName': 'ves',
                 'translitValue': 'bolee-51-kg', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Цвет', 'selected': False, 'translitName': 'cvet', 'type': 'cvet', 'codes': [89], 'criterias': [
                {'name': 'черный', 'value': 'черный', 'count': 0, 'translitName': 'cvet', 'translitValue': 'chernyi',
                 'selected': False, 'isSeo': True},
                {'name': 'синий', 'value': 'синий', 'count': 0, 'translitName': 'cvet', 'translitValue': 'sinii',
                 'selected': False, 'isSeo': True},
                {'name': 'зеленый', 'value': 'зеленый', 'count': 0, 'translitName': 'cvet', 'translitValue': 'zelenyi',
                 'selected': False, 'isSeo': True},
                {'name': 'разноцветный', 'value': 'разноцветный', 'count': 0, 'translitName': 'cvet',
                 'translitValue': 'raznocvetnyi', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Товары со скидкой', 'selected': False, 'translitName': 'skidka', 'type': 'razmer-skidki',
             'codes': [-8],
             'criterias': [{'name': 'Более 30%', 'value': 'Более 30%', 'count': 0, 'translitName': 'razmer-skidki',
                            'translitValue': 'bolee-30', 'selected': False, 'isSeo': True},
                           {'name': 'Более 10%', 'value': 'Более 10%', 'count': 0, 'translitName': 'razmer-skidki',
                            'translitValue': 'bolee-10', 'selected': False, 'isSeo': True},
                           {'name': 'Более 5%', 'value': 'Более 5%', 'count': 0, 'translitName': 'razmer-skidki',
                            'translitValue': 'bolee-5', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Продавец', 'selected': False, 'translitName': 'prodavec', 'type': 'prodavec', 'codes': [-14],
             'criterias': [
                 {'name': 'Другой продавец', 'value': 'Другой продавец', 'count': 0, 'translitName': 'prodavec',
                  'translitValue': 'drugoi-prodavec', 'selected': False, 'isSeo': True}],
             'urlFacetCrossBlock': None},
            {'name': 'Только в наличии', 'selected': True, 'translitName': 'tolko-v-nalichii',
             'type': 'tolko-v-nalichii',
             'codes': [-9], 'criterias': [
                {'name': 'Да', 'value': 'Да', 'translitName': 'tolko-v-nalichii', 'translitValue': 'da',
                 'selected': True,
                 'isSeo': False}], 'urlFacetCrossBlock': None},
            {'name': 'Забрать через 15 минут', 'selected': True, 'translitName': 'zabrat-cherez-15-minut',
             'type': 'zabrat-cherez-15-minut', 'codes': [-11], 'criterias': [
                {'name': 'S972', 'value': 'S972', 'translitName': 'zabrat-cherez-15-minut', 'translitValue': 'S972',
                 'selected': True, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Забрать из магазина по адресу', 'selected': True, 'translitName': 'zabrat-iz-magazina-po-adresu',
             'type': 'zabrat-iz-magazina-po-adresu', 'codes': [-12], 'criterias': [
                {'name': 'S659', 'value': 'S659', 'count': 0, 'translitName': 'zabrat-iz-magazina-po-adresu',
                 'translitValue': 'S659', 'selected': True, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Доставить курьером', 'selected': False, 'translitName': 'dostavit-kurerom',
             'type': 'dostavit-kurerom',
             'codes': [-13], 'criterias': [
                {'name': 'Да', 'value': 'Да', 'translitName': 'dostavit-kurerom', 'translitValue': 'da',
                 'selected': False,
                 'isSeo': False}], 'urlFacetCrossBlock': None},
            {'name': 'Рейтинг покупателей', 'selected': False, 'translitName': 'reiting-pokupatelei',
             'type': 'reiting-pokupatelei', 'codes': [-4], 'criterias': [
                {'name': 'От', 'value': 'От 4', 'count': 0, 'translitName': 'reiting-pokupatelei',
                 'translitValue': 'ot-4',
                 'selected': False, 'isSeo': False},
                {'name': 'От', 'value': 'От 3', 'count': 0, 'translitName': 'reiting-pokupatelei',
                 'translitValue': 'ot-3',
                 'selected': False, 'isSeo': True},
                {'name': 'От', 'value': 'От 2', 'count': 0, 'translitName': 'reiting-pokupatelei',
                 'translitValue': 'ot-2',
                 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None},
            {'name': 'Подборки', 'selected': False, 'translitName': 'collection_bottom', 'type': 'collection_bottom',
             'codes': [-6], 'criterias': [
                {'name': 'для взрослых', 'value': 'для взрослых', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'dlya-vzroslyh', 'selected': False, 'isSeo': True},
                {'name': 'для дачи', 'value': 'для дачи', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'dlya-dachi', 'selected': False, 'isSeo': True},
                {'name': 'каркасные', 'value': 'каркасные', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'karkasnye', 'selected': False, 'isSeo': True},
                {'name': 'круглые', 'value': 'круглые', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'kruglye', 'selected': False, 'isSeo': True},
                {'name': 'с сеткой', 'value': 'с сеткой', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 's-setkoi', 'selected': False, 'isSeo': True},
                {'name': 'до 150 кг', 'value': 'до 150 кг', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'do-150-kg', 'selected': False, 'isSeo': True},
                {'name': '10 FT', 'value': '10 FT', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '10-ft',
                 'selected': False, 'isSeo': True},
                {'name': '10 футов', 'value': '10 футов', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '10-futov', 'selected': False, 'isSeo': True},
                {'name': '3 м', 'value': '3 м', 'count': 0, 'translitName': 'collection_bottom', 'translitValue': '3-m',
                 'selected': False, 'isSeo': True},
                {'name': '4 м', 'value': '4 м', 'count': 0, 'translitName': 'collection_bottom', 'translitValue': '4-m',
                 'selected': False, 'isSeo': True},
                {'name': '2.5 м', 'value': '2.5 м', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '25-m',
                 'selected': False, 'isSeo': True},
                {'name': '8 ft (244 см)', 'value': '8 ft (244 см)', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '8-ft-244-sm', 'selected': False, 'isSeo': True},
                {'name': '12 ft (366 см)', 'value': '12 ft (366 см)', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '12-ft-366-sm', 'selected': False, 'isSeo': True},
                {'name': '14 FT', 'value': '14 FT', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '14-ft',
                 'selected': False, 'isSeo': True},
                {'name': '16 FT', 'value': '16 FT', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '16-ft',
                 'selected': False, 'isSeo': True},
                {'name': 'большие', 'value': 'большие', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'bolshie', 'selected': False, 'isSeo': True},
                {'name': '6 FT', 'value': '6 FT', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '6-ft',
                 'selected': False, 'isSeo': True},
                {'name': 'без сетки', 'value': 'без сетки', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '', 'selected': False, 'isSeo': True},
                {'name': 'маленькие', 'value': 'маленькие', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'malenkie', 'selected': False, 'isSeo': True},
                {'name': '120 кг', 'value': '120 кг', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': '120-kg', 'selected': False, 'isSeo': True},
                {'name': 'для джампинга', 'value': 'для джампинга', 'count': 0, 'translitName': 'collection_bottom',
                 'translitValue': 'dlya-dzhampinga', 'selected': False, 'isSeo': True}], 'urlFacetCrossBlock': None}
        ],
        'categories': [
            {
                'id': '31018', 'count': 0, 'name': 'Товары для активного отдыха',
                'children': [
                    {
                        'id': '23715',
                        'count': 0,
                        'name': 'Батуты',
                        'children': [
                            {
                                'id': '23716', 'count': 0, 'name': 'Батуты', 'children': [],
                                'translitName': 'batuty', 'isSeo': True
                            },
                            {
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

#  https://www.mvideo.ru/sitemaps/sitemap-categories-www.mvideo.ru-1.xml

# url_count_settings = f'https://www.mvideo.ru/bff/settings?types=plp' ( акие то есть категории но не все мало)
# url_count_settings = f'https://www.mvideo.ru/bff/product-details/list'  # (похоже что здесь все категории, но метод POST)
# 'https://www.mvideo.ru/bff/settings/v2/catalog'
# Структура:
# Айди категории: json_python['body']['products']['categories']['id']
# Имя категории: json_python['body']['products']['categories']['name']
# Имя категории: json_python['body']['products']['groups']['name']


# json_python = q.get_response_json__(url_count_settings)
# print(json_python)