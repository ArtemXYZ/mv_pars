

from parser_04_vers.facade import MvPars

pars = MvPars()
pars.activate.run_one_cycle_pars(load_damp=False)  # , if_exists='append'

pars.activate.preparate_results_df()
pars.activate.upload_to_db()







