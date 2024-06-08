from collections import defaultdict
import pandas as pd

def get_unique_legal_files(aup_df, exp_df):
    unique_aup_legal_files_dict_in_aup = {}
    unique_aup_legal_files_dict_in_exp = {}
    aup_total_legal_files_dict_in_aup = defaultdict(list)
    exp_total_legal_files_dict_in_exp = defaultdict(list)

    # 1. Unique aup dict
    # Get all of the columns with paths/files
    aup_path_columns = [col for col in aup_df.columns if 'file' in col.lower()]

    # Get all of the files grouped by main cid for AUP
    for index, row in aup_df.iterrows():
        main_cid = row['Main CID']
        paths = [row[col] for col in aup_path_columns if pd.notna(row[col]) and row[col] != '-']
        if paths:
            aup_total_legal_files_dict_in_aup[main_cid].extend(paths)

    # Convert to unique paths for AUP
    for cid, paths in aup_total_legal_files_dict_in_aup.items():
        unique_aup_legal_files_dict_in_aup[cid] = list(set(paths))

    # 2. Unique exp dict
    # Get all of the columns with paths/files
    exp_path_columns = [col for col in exp_df.columns if 'file' in col.lower()]

    # Get all of the files grouped by main cid for EXP
    for index, row in exp_df.iterrows():
        main_cid = row['Main CID']
        paths = [row[col] for col in exp_path_columns if pd.notna(row[col]) and row[col] != '-']
        if paths:
            exp_total_legal_files_dict_in_exp[main_cid].extend(paths)

    # Convert to unique paths for EXP
    for cid, paths in exp_total_legal_files_dict_in_exp.items():
        unique_aup_legal_files_dict_in_exp[cid] = list(set(paths))

    return unique_aup_legal_files_dict_in_exp, unique_aup_legal_files_dict_in_aup
