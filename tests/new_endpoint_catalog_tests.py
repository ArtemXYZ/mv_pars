"""
    Исследование нового ендпоинта Мвидео на предоставление каталога товаров (по конкретному филиалу)
"""

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

category_id = 205
url_new_construct = f'https://www.mvideo.ru/bff/products/v2/search?categoryIds={category_id}&offset=0'

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


# =========================================================== # todo тест старого url
#

class OldUrlTest:

    __session: Session = requests.Session()  # Экземпляр сессии:
    __base_headers = BASE_HEADERS

    def get_response_json__(self, url: str = None, params: dict = None, cookies: dict = None) -> object:
        """Функция для запросов с мутабельными параметрами. """

        # Устанавливаем куки в сессии (если были переданы):
        if cookies:
            self.__session.cookies.update(cookies)

        try:
            # Выполнение запроса с сессией
            response = self.__session.get(url=url, headers=self.__base_headers, params=params)
            # Проверка кода ответа
            if response.status_code == 200:
                data = response.json()  # Ответ в формате JSON

            else:
                # Обработка некорректных HTTP ответов
                raise requests.exceptions.HTTPError(f"Ошибка HTTP: {response.status_code} - {response.text}")

        # Перехватываем любые ошибки, включая сетевые и прочие исключения
        except Exception as error_connect:
            raise  # Передача исключения на верхний уровень для обработки
        return data

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

    def count_product_request__(self, category_id, id_branch, city_id, region_id, region_shop_id, timezone_offset):
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
        url_count = f'https://www.mvideo.ru/bff/products/listing?categoryId={category_id}&offset=0&limit=1'
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


    # @staticmethod
    # def _run_one_cycle_pars(df_full_branch_data, city_id, if_exists='replace'):  # get_category append replace
    #
    #
    #     # Кортеж категорий на исключение (наполнение через итерации):
    #     bag_category_tuple = ()
    #
    #     # Создаем целевой итоговый датафрейм, куда будут сохранены данные типа: код магазина, категория (имя),
    #     # количество.
    #     df_fin_category_data = pd.DataFrame(
    #         columns=[
    #             'id_branch',
    #             'name_category',  # Подлежит удалению, добавлена будет в др. таблицу
    #             'count',
    #             'parent_category_id',
    #             'category_id',
    #         ]
    #     )
    #
    #
    #     # 2) Подготовка данных (очистка и иерации):
    #     # ----------------------------------------------------------
    #     # Удаляем строки, где city_id равен 0
    #     df_branch_not_null = df_full_branch_data[df_full_branch_data['city_id'] != 0]
    #     # Если нужно удалить строки в исходном DataFrame (на месте):
    #     # df_full_branch_data.drop(df_full_branch_data[df_full_branch_data['city_id'] == 0].index, inplace=True)
    #
    #     # Создаем целевой сириес для id категорий: - лишком тяжелый, проще обычный список перебрать.
    #     # df_category_id_data = pd.DataFrame(CATEGORY_ID_DATA, columns=['category_id'])
    #     # ----------------------------------------------------------
    #
    #     # 3) Основная конструкция перебирания филиалов по категориям\
    #     # 3.1) Итерируем по категориям (на каждую категорию итерируем по филиалам) :
    #     # ----------------------------------------------------------
    #
    #     # for row in CATEGORY_ID_DATA:
    #
    #     for row in tqdm(CATEGORY_ID_DATA, total=len(CATEGORY_ID_DATA), ncols=80, ascii=True,
    #                     desc=f'==================== Обработка данных по категории ===================='):
    #
    #         time.sleep(0.1)  # \n
    #         # Забирает id категории верхнего уровня в структуре МВидео\
    #         # (подставляется в ендпоинт, что бы получить "category_id"):
    #         parent_category_id = row  # бывшая category_id
    #
    #         print(f'\n==================== Родительская категория {parent_category_id} ====================')
    #         print(f'==================== Обработка данных филиалов  ====================')
    #
    #         # 3.1.1) Итерируем по филиалам и по конкретной категории:
    #         for index, row in df_branch_not_null.iterrows():
    #             # for index, row in tqdm(df_branch_not_null.iterrows(), ncols=80, ascii=True,
    #             #          desc=f'=================================================================='):
    #             # desc=f'==================== Обработка данных филиала ===================='):
    #
    #             # Достаем данные из строки датафрейма:
    #             id_branch = row.get('id_branch')
    #             city_name_branch = row.get('city_name_branch')
    #             city_id = row.get('city_id')
    #             region_id = row.get('region_id')
    #             region_shop_id = row.get('region_shop_id')
    #             timezone_offset = row.get('timezone_offset')
    #
    #             # Случайная задержка для имитации человека:
    #             self._get_time_sleep_random()
    #
    #             # 3.1.1.1) Основной запрос (возвращает json (пайтон)):
    #             json_python = self._count_product_request(parent_category_id, id_branch, city_id, region_id,
    #                                                       region_shop_id, timezone_offset)
    #             # print(json_python)
    #             # ----------------------------------------------------------
    #
    #             # 4) Обработка и сохранение результатов (достаем нужные категории и сохраняем в итоговый датафрейм)
    #             # ----------------------------------------------------------
    #             if json_python:
    #
    #                 # category_id_
    #
    #                 # Обращаемся к родительскому ключу, где хранятся категории товаров:
    #                 all_category_in_html = json_python['body']['filters'][0]['criterias']
    #                 # print(f'Все категории на странице: {all_category_in_html}')
    #
    #                 try:
    #                     # Перебираем родительскую директорию, забираем значения категорий и количество:
    #                     for row_category in all_category_in_html:
    #
    #                         # 1. # Количество по категории (если != 'Да' \
    #                         # то здесь все равно будет None, условие проверки не нужно, опускаем).
    #                         count = row_category['count']
    #
    #                         # 2. Наименование категории: если count равно 'Да', то name_category также будет None
    #                         name_category = None if row_category['name'] == 'Да' else row_category['name']
    #
    #                         # 3. id искомой категории (получена от родительской):
    #                         category_id = row_category['value']  # ключ 'value' = id
    #
    #
    #                         new_row = {
    #                             'id_branch': id_branch,
    #                             'name_category': name_category,
    #                             'count': count,
    #                             'parent_category_id': parent_category_id,
    #                             'category_id': category_id
    #                         }
    #
    #                         # print(f'count: {count}, name {name_category}')
    #                         print(f'{index}. {new_row}')
    #                         # Сохраняем в целевой итоговый датафырейм:
    #                         # Добавляем новую строку с помощью loc[], где индексом будет len(df_fin_category_data)
    #                         df_fin_category_data.loc[len(df_fin_category_data)] = new_row
    #
    #
    #                 except (KeyError, IndexError):
    #                     # Срабатывает, если ключ 'criterias' не существует или его невозможно получить
    #                     print(f'По parent_category_id {parent_category_id} - нет нужных тегов, пропускаем ее.')
    #
    #                     # Добавление в общий кортеж багов.
    #                     bag_category_tuple = bag_category_tuple + (parent_category_id,)
    #
    #             else:
    #                 # row_bag_iter = new_row
    #                 print(f'Пропуск итерации для: {id_branch} city_name_branch {city_name_branch}')
    #                 continue
    #             # break  #  Для теста - оба брейка нужны
    #             # Итог код магазина, категория, количество. ['id_branch','name_category','count']
    #             # ----------------------------------------------------------
    #         # break #  Для теста - оба брейка нужны
    #     # Если по конкретной категории не нашлись нужные теги, такая категория добавится в список.
    #     # Далее эти категории можно исключить из парсинга.
    #     print(f'Список лишних категорий: {bag_category_tuple}.')
    #
    #     # Итог код магазина, категория, количество. ['id_branch','name_category','count']
    #     return df_fin_category_data
    # __________________________________________________________________



# 3.1.1.1) Основной запрос (возвращает json (пайтон)):
oldurl = OldUrlTest()

json_python = oldurl.count_product_request__(
    # Бузулук, ул. Комсомольская, д. 81, ТРЦ «Север»
    category_id='205',
    id_branch='S659',
    city_id='CityDE_31010',
    region_id='4',
    region_shop_id='S972',
    timezone_offset='4'
)


# print(json_python)

# Обращаемся к родительскому ключу, где хранятся категории товаров:
all_category_in_html = json_python['body']['filters'][0]['criterias'][0]['value']

print(all_category_in_html)

json_python_response = \
    {'success': True,
     'messages': [],
     'body':
         {
             'type': 'plain',
             'total': 116,
             'products': ['30074328', '30074463', '30074447',
                          '400378297', '400307031',
                          '30077266', '30074464', '30074444',
                          '30074445', '400340348',
                          '30077269', '400259093', '400268685',
                          '30070496', '30074325',
                          '400291228', '30074466', '400335295',
                          '400307053', '400326918',
                          '30070480', '400365681', '400378331',
                          '400407107', '400259098',
                          '400329255', '30070624', '400405852',
                          '30077721', '400255430',
                          '400340382', '400407204', '400407106',
                          '400282912', '400288613',
                          '400394468'],
             'filters': [
                 {'name': 'Категория',
                  'selected': False,
                  'translitName': 'category',
                  'type': 'category',
                  'codes': [-14],
                  'criterias': [
                      {
                          'name': 'Смартфоны', 'value': '761', 'count': 100, 'translitName': 'smartfony',
                          'translitValue': '761', 'selected': False, 'isSeo': True
                      },
                      {
                          'name': 'iPhone', 'value': '914', 'count': 16, 'translitName': 'iphone',
                          'translitValue': '914',
                          'selected': False, 'isSeo': True
                      }
                  ],
                  'urlFacetCrossBlock': {'excluded': []}
                  }
             ]}
     }
