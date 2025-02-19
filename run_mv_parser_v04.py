

from parser_04_vers.facade import MvPars

pars = MvPars()
pars.activate.run_one_cycle_pars(load_damp=True)  # , if_exists='append'



# catalog_df = pars.activate.preparate_results_df_to_catalog()
# pars.activate.save_catalog_df_in_db(catalog_df)

# Загрузить результаты последнего парсинга или спарсить заново.





