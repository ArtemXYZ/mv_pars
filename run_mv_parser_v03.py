from parser_03_vers.facade import MvPars
from data.dir import base_dir

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
# pars.activate.run_week_cycle_pars()

# wed - среда
# sun -
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
pars = MvPars()
# pars.set.set_ping_limits(2.5, 3.5)
# pars.info.get_timeout
# pars.activate.get_branches_dat()   # +
pars.activate.run_one_cycle_pars(load_damp=True)
# pars.activate.run_week_cycle_pars(day_of_week='wed',hour=9, minute=9) # 'sun'
pars.set.set_base_folder_save(base_dir)




# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------







