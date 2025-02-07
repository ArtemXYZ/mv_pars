from parser_03_vers.base_property import BaseProperty

import re
import requests
import json
import base64  # переопределяется (зацикливание)
import urllib.parse  # переопределяется (зацикливание)
from datetime import datetime  # переопределяется (зацикливание)
import os
import requests
import pandas as pd
from pandas import DataFrame
import time
# from bs4 import BeautifulSoup
from joblib import dump
from joblib import load
# from apscheduler.triggers.cron import CronTrigger

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class ServiceTools(BaseProperty):
    """Вспомогательные методы вынесены в отдельный класс."""

    def __init__(self):
        super().__init__()  # Наследуем атрибуты из BaseProperty

        self.__session = self._get_session()  # Экземпляр сессии:
        self.__base_headers = self._get_headers()
        self.__name_table = self._get_name_table()
        self.__schema = self._get_name_schem()
        self.__con = self._get_connect()
        # self.__bloc_scheduler = self._get_scheduler()
        # self.__cron_trigger = self._get_cron_trigger


        # pass

    # __________________________________________________________________ TOOLS
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
            data_list_dict: list[dict, ...] = xml_content['urlset']['url']

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

