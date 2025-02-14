# """Основные функции вынесены в отдельный модуль."""
# # ----------------------------------------------------------------------------------------------------------------------
# import time
# import random
# # import undetected_chromedriver
# # from selenium.webdriver.common.by import By
#
# # ----------------------------------------------------------------------------------------------------------------------
# # Устанавливаем путь к драйверу браузера
# # driver_und = undetected_chromedriver.Chrome(version_main=121)
#
#
# # ----------------------------------------------------------------------------------------------------------------------
#
#
# # -----------------------------------------------------------------------
# # Получаем количество товара по категориям:
# def get_undetected_sup_by_html_category(branch, region_shop, category_part):
#     """
#     """
#
#     url_base = 'https://www.mvideo.ru'
#
#     # Динамически изменяемые параметры.
#     full_url_no_param = (f'{url_base}{category_part}?'
#                          f'f_tolko-v-nalichii=da&'
#                          f'f_zabrat-iz-magazina-po-adresu={branch}&'
#                          f'f_zabrat-cherez-15-minut={region_shop}'
#                          )
#
#     try:
#
#         time.sleep(random.uniform(1.0, 3.0))
#
#         driver_und.get(full_url_no_param)
#
#         time.sleep(10)  # Задержка 1 секунды
#
#
#
#         # Пример получения нужного элемента с помощью современного синтаксиса
#         # span_tag = driver_und.find_element(By.CSS_SELECTOR, "span.count.ng-star-inserted")
#
#         # span_tag = driver_und.find_element(By.CSS_SELECTOR, "span.count")
#         # print(f"Значение: {span_tag.text}")
#         print(driver_und.page_source)
#
#     except Exception as erx:
#         print(f'Ошибка в "get_undetected_sup_by_html_category": {erx}')
#         # driver_und.quit()  # Закрытие браузера
#     finally:
#
#         time.sleep(2)  # Задержка 1 секунды
#         driver_und.close()
#         driver_und.quit()  # Закрытие браузера
#
#     # return span_tag
#
#
# #
