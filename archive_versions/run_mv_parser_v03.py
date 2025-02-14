from parser_04_vers.facade import MvPars
# from data.dir import base_dir

# Справочно:
# ----------------------------------------------------------------------------------------------------------------------
# pars = MvPars()

# 1) Активация выдачи информации о текущих параметрах:
# pars.info.get_headers
# pars.info.get_name_table
# и тд.

# 2) Активация установки новых параметров:
# pars.set.set_table('abs').set_base_folder_save('../data/').set_ping_limits(2.5, 3.5) ... и тд.

# 3) Активация работы основных функций:
# pars.activate.get_branches()
# pars.activate.run_one_cycle_pars()

# ----------------------------------------------------------  устарело:
# pars.activate.run_week_cycle_pars()

# Точные сокращения для планировщика:
# wed - среда
# sun - воскресенье

# pars.activate.run_week_cycle_pars(day_of_week='wed',h=9, m=0) # 'sun'
# pars.set.set_base_folder_save(base_dir)

# крон не работает только интервал в 7 дней (проблема в сторонней библиотеке)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
pars = MvPars()
# pars.set.set_ping_limits(2.5, 3.5)
# pars.info.get_timeout
# pars.activate.get_branches_dat()   # +

# Выбираем метод 'replace' для перезаписи таблицы или 'append' для добавления данных,
# по умолчанию всегда 'replace' (можно не указывать)
# pars.activate.run_one_cycle_pars(load_damp=True, if_exists='append')  # , if_exists='append'



# pars.activate.run_week_pars_interval(7)   # todo: крон не работает только интервал в 7 дней


# print(pars.info.get_path_file_category_dump)  # ./data/df_category_data.joblib
# print(pars.set.set_unified_names_files_for_category())
# print(pars.info.get_path_file_category_dump)

# pars.activate.load_result_pars_in_db(name_path_file_dump='./data/df_category_data.joblib', if_exists='append')  #
# pars.activate.load_result_pars_in_db(if_exists='append')

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------







