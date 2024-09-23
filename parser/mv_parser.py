

class MvPars:

    _expansion_file_dump = '.joblib'
    _expansion_file_excel = '.joblib'

    base_folder_save = f'../data/'


    save_name_dump_branch_data = 'df_branch_data'
    save_name_excel_branch_data = 'df_branch_data'

    save_name_dump_category_data = 'df_category_data'
    save_name_excel_category_data = 'df_category_data'

    full_path_dump_branch_data = base_folder_save + save_name_dump_branch_data + _expansion_file_dump
    _full_path_dump_category_data = ''



    def get_file_name(self):
        _name_dump = f'../data/{save_name_dump}.joblib'
        _name_excel = f'../data/{save_name_excel}.xlsx'

    # Создаём сессию
    session = requests.Session()