from parser_03_vers.base_property import BaseProperty
from parser_03_vers.parsing_patterns import ParsingPatterns


# from parser_03_vers.service_tools import ServiceTools


# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
class InfoManager(BaseProperty):
    """
    Класс для управления информацией, такой как заголовки запросов.
    """

    def __init__(self):
        super().__init__()  # Обязательно нужен, т.к. используется при вызове в MvPars()

    @property
    def get_retries(self):
        return self._get_retries()

    @property
    def get_timeout(self):
        return self._get_timeout()

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
        super().__init__()  # Обязательно нужен, т.к. используется при вызове в MvPars()

    def set_timeout(self, new_timeout_param):
        self._set_timeout(new_timeout_param)
        return self

    def set_retries(self, new_retries_param):
        self._set_retries(new_retries_param)
        return self

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
        print(f'Установлено новое значение имени папки для сохранения результатов работы парсера: {new_folder}')
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
        super().__init__()  # Обязательно нужен, т.к. используется при вызове в MvPars()

    def get_branches_dat(self):
        return self._get_branches_dat()

    def run_one_cycle_pars(self, load_damp=False, if_exists='replace'):
        return self._run_one_cycle_pars(load_damp=load_damp, if_exists=if_exists)

    def run_week_cycle_pars(self, day_of_week=None, h=None, m=None):   # cron_string=None):
        # Работаем со значениями по умолчанию:
        # if cron_string is None:
        if day_of_week is None and h is None and m is None:
            # 5 14 * * 2
            # Если не назначены значения времени, то вызываем метод (со значениями по умолчанию):
            self._run_week_cycle_pars()
        else:

            # self._run_week_cycle_pars(cron_string)
            self._run_week_cycle_pars(week=day_of_week, hour=h, minute=m)
            print(f'Для планировщика обновлено значение запуска '
                  f'day_of_week: {day_of_week}, hour: {h}, minute: {m}.')

    def run_week_cycle_pars_cron(self, cron_string=None):  # 5 14 * * 2
        # Работаем со значениями по умолчанию:
        if not cron_string:  # if cron_string is None:
            # Если не назначены значения времени, то вызываем метод (со значениями по умолчанию):
            self._run_week_cycle_pars_cron()
        else:
            # self._run_week_cycle_pars(cron_string)
            self._run_week_cycle_pars_cron(cron_string=cron_string)
            print(f'Для планировщика обновлено значение запуска: {cron_string}')

    def run_week_pars_cron(self, cron_string='00 23 * * 6'):
        self._run_week_pars_cron(cron_string=cron_string)


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
        print('Класс фасад.')
# ----------------------------------------------------------------------------------------------------------------------