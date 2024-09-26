
    # ------------------------------------------------------
    # @classmethod
    # def _get_file_name(cls, folder=None, name=None, expansion=None):
    #     # create_path_name
    #     return f'{folder}{name}{expansion}'

    # # ------------------------------------------------------
    # # instance - передаем экземпляр в метод, чтобы использовать его атрибуты.
    # @classmethod
    # def _get_file_name_branch_dump(cls, instance):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_dump_branch_data,
    #                                  cls.__EXPANSION_FILE_DUMP)
    #
    # @classmethod
    # def _get_file_name_branch_excel(cls, instance):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_branch_data,
    #                               cls.__EXPANSION_FILE_EXCEL)
    #
    # @classmethod
    # def _get_file_name_category_dump(cls, instance):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_dump_category_data,
    #                               cls.__EXPANSION_FILE_DUMP)
    #
    # @classmethod
    # def _get_file_name_category_excel(cls, instance):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_category_data,
    #                               cls.__EXPANSION_FILE_EXCEL)
    # # ------------------------------------------------------










# MvPars.get_response()
# pars = BranchesDat()
# pars.get_shops()
# a = pars.ping_min(0,3) # Добавить в методы разные проверки.
# pars.name_file

# ----------------------------------------------------------------------------------------------------------------------
#     @staticmethod
#     def get_response(self,
#                      url: str, headers: dict = None, params: dict = None, cookies: dict = None, session=None,
#                      json_type=True) -> object:
#         """Универсальная функция для запросов с передаваемыми параметрами. """
#
#         self.url = url
#         self.headers = headers
#         self.params = params
#         self.cookies = cookies
#         self.session = session
#         self.json_type = json_type
#
#         # Устанавливаем куки в сессии
#         if self.session and self.cookies:
#             self.session.cookies.update(self.cookies)
#
#         # Обычный запрос или сессия:
#         if self.session:
#             response = self.session.get(self.url, headers=self.headers, params=self.params)
#
#         else:
#             response = requests.get(self.url, headers=self.headers, params=self.params, cookies=self.cookies)
#
#         # Выполнение запроса:
#         if response.status_code == 200:
#
#             if self.json_type:
#                 # Если ответ нужен в json:
#                 data = response.json()
#
#             elif not self.json_type:
#                 # Если ответ нужен в html:
#                 data = response.text
#
#         else:
#             data = None
#             print(f"Ошибка: {response.status_code} - {response.text}")
#
#         return data


# class Response:
#
#
#     def __init__(self):
#         pass
#
#     def get_response(self,
#                      url: str, headers: dict = None, params: dict = None, cookies: dict = None, session=None,
#                      json_type=True) -> object:
#
#         """Универсальная функция для запросов с передаваемыми параметрами. """
#
#         self.url = url
#         self.headers = headers
#         self.params = params
#         self.cookies = cookies
#         self.session = session
#         self.json_type = json_type
#
#
#         # Устанавливаем куки в сессии
#         if self.session and self.cookies:
#             self.session.cookies.update(cookies)
#
#         # Обычный запрос или сессия:
#         if self.session:
#             response = self.session.get(url, headers=headers, params=params)
#
#         else:
#             response = requests.get(url, headers=headers, params=params, cookies=cookies)
#
#
#         # Выполнение запроса:
#         if response.status_code == 200:
#
#             if self.json_type:
#                 # Если ответ нужен в json:
#                 data = response.json()
#
#             elif not self.json_type:
#                 # Если ответ нужен в html:
#                 data = response.text
#                 # print(f'{data}')
#
#         else:
#             data = None
#             print(f"Ошибка: {response.status_code} - {response.text}")
#
#         return data
# cookies_get_shops: dict,  #=cookies_shops,

# def get_file_name_branch_dump(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_dump_branch_data, self.__EXPANSION_FILE_DUMP)
#
#     def get_file_name_branch_excel(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_excel_branch_data,
#                                     self.__EXPANSION_FILE_EXCEL)
#
#     def get_file_name_category_dump(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_dump_category_data,
#                                     self.__EXPANSION_FILE_DUMP)
#
#     def get_file_name_category_excel(self):
#         return MvPars.get_file_name(self.base_folder_save, self.save_name_excel_category_data,
#                                     self.__EXPANSION_FILE_EXCEL)



#     # Методы для получения файловых путей с использованием значений по умолчанию
#     def get_file_name_branch_dump(self):
#         return self._get_file_name(self._BASE_FOLDER_SAVE, self._save_name_dump_branch_data, self._EXTENSION_FILE_DUMP)
#
#     def get_file_name_branch_excel(self):
#         return self._get_file_name(self._BASE_FOLDER_SAVE, self._save_name_excel_branch_data, self._EXTENSION_FILE_EXCEL)
#
#     # Методы для изменения значений по умолчанию
#     def set_save_name_dump_branch_data(self, new_name: str):
#         self._save_name_dump_branch_data = new_name
#
#     def set_save_name_excel_branch_data(self, new_name: str):
#         self._save_name_excel_branch_data = new_name
#
#     def set_ping_limits(self, ping_min: float, ping_max: float):
#         self._imitation_ping_min = ping_min
#         self._imitation_ping_max = ping_max


# ------------------------------------------------------
    # # instance - передаем экземпляр в метод, чтобы использовать его атрибуты.
    # @staticmethod
    # def _get_file_name_branch_dump():
    #     return cls._get_file_name(base_folder_save, save_name_dump_branch_data,
    #                               ParsTools()._EXPANSION_FILE_DUMP)
    #
    # @staticmethod
    # def _get_file_name_branch_excel( ):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_branch_data,
    #                               cls._EXPANSION_FILE_EXCEL)
    #
    # @staticmethod
    # def _get_file_name_category_dump( ):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_dump_category_data,
    #                               cls._EXPANSION_FILE_DUMP)
    #
    # @staticmethod
    # def _get_file_name_category_excel(cls, instance):
    #     return cls._get_file_name(instance.base_folder_save, instance.save_name_excel_category_data,
    #                               cls._EXPANSION_FILE_EXCEL)
    # ------------------------------------------------------

    #     def get_file_name_branch_dump(self, base_folder=None, name_file=None, extension=None):
    #     """
    #     Формирует путь для сохранения дампа по филиалам.
    #     Если необходимо изменить путь, вызываем данный метод и перезаписываем переменные.
    #     """
    #
    #     self.base_folder = base_folder if base_folder else self._BASE_FOLDER_SAVE
    #     self.name_file = name_file if name_file else self.get_file_name_branch()
    #     self.extension = extension if extension else self._EXTENSION_FILE_DUMP
    #
    #     return self._get_file_name_path(self.base_folder, self.name_file, self.extension)
    #
    # def get_file_name_branch_excel(self, base_folder=None, name_file=None, extension=None):
    #     """
    #     Формирует путь для сохранения файла excel по филиалам.
    #     Если необходимо изменить путь, вызываем данный метод и перезаписываем переменные.
    #     """
    #
    #     self.base_folder = base_folder if base_folder else self._BASE_FOLDER_SAVE
    #     self.name_file = name_file if name_file else self.get_file_name_branch()
    #     self.extension = extension if extension else self._EXTENSION_FILE_EXCEL
    #
    #     return self._get_file_name_path(self.base_folder, self.name_file, self.extension)