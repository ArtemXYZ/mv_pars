from parser_new.base_property import BaseProperty
from parser_new.parsing_patterns import ParsingPatterns


# from parser_new.service_tools import ServiceTools


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class InfoManager(BaseProperty):
    """
    Класс для управления информацией, такой как заголовки запросов.
    """

    def __init__(self):
        super().__init__()  # Обязательно нужен, т.к. используется привызове в MvPars()

    @property
    def get_category_id_data(self):
        return self._get_category_id_data()

    @property
    def get_connect(self):
        return self._get_connect()

    @property
    def get_name_table(self):
        return self._get_name_table()

    @property
    def get_schem(self):
        return self._get_name_schem()

    @property
    def get_city_data(self):
        return self._get_city_data()

    @property
    def get_base_folder(self):
        return self._get_base_folder_save()

    @property
    def get_headers(self):
        return self._get_headers()

    @property
    def get_unified_names_files_for_branches(self):
        return self._get_unified_names_files_for_branches()

    @property
    def get_unified_names_files_for_category(self):
        return self._get_unified_names_files_for_category()

    @property
    def get_path_file_branch_dump(self):
        return self._get_path_file_branch_dump()

    @property
    def get_path_file_category_dump(self):
        return self._get_path_file_category_dump()

    @property
    def get_ping_limits(self):
        return self._get_ping_limits()

    @property
    def get_time_sleep_random(self):
        return self._get_time_sleep_random()


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class PropertyManager(BaseProperty):
    """
    Класс для управления свойствами парсера.
    """

    def __init__(self):
        super().__init__()  # Обязательно нужен, т.к. используется привызове в MvPars()

    def set_category_id_data(self, new_category_data):
        self._set_category_id_data(new_category_data)
        return self

    def set_new_connect(self, new_connect_obj):
        self._set_connect(new_connect_obj)
        return self

    def set_table(self, new_name_table):
        self._set_name_table(new_name_table)
        return self

    def set_schem(self, new_name_schem):
        self._set_name_schem(new_name_schem)
        return self

    def set_city_data(self, new_city_data):
        self._set_city_data(new_city_data)
        return self

    def set_base_folder_save(self, new_folder):
        self._set_base_folder_save(new_folder)
        return self

    def set_headers(self, new_headers):
        self._set_headers(new_headers)
        return self

    def set_unified_names_files_for_branches(self, new_name_file):
        self._set_unified_names_files_for_branches(new_name_file)
        return self

    def set_unified_names_files_for_category(self, new_name_file):
        self._set_unified_names_files_for_category(new_name_file)
        return self

    def set_ping_limits(self, min_ping, max_ping):
        self._set_ping_limits(min_ping, max_ping)
        return self


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class ActivateManager(ParsingPatterns):
    """
    Класс для активации и управления выполнением задач.
    """

    def __init__(self):
        super().__init__()  # Обязательно нужен, т.к. используется привызове в MvPars()

    def get_branches_dat(self):
        return self._get_branches_dat()

    def run_one_cycle_pars(self):
        return self._run_one_cycle_pars()

    def run_week_cycle_pars(self):
        # Расписание работы
        return self._run_week_cycle_pars()


# ----------------------------------------------------------------------------------------------------------------------
# ***
# ----------------------------------------------------------------------------------------------------------------------
class MvPars:
    """
    Парсинг количества товаров на остатке по филиалам по расписанию.
    """

    # ------------------------------------------------------
    def __init__(self):
        # super().__init__()
        self.info = InfoManager()
        self.set = PropertyManager()
        self.activate = ActivateManager()

    def __repr__(self):
        print('Класс фаcад.')


# ----------------------------------------------------------------------------------------------------------------------

