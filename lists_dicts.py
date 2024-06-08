
import os 
import re
import hashlib
import pandas as pd
# Lists,dicts

# DFs  
# Mapping Df (needs a pivoted excel file) (get the main cid and its relevant cids)
exp_excel_file = r"suezf.xlsx"
exp_mapping_df = pd.read_excel(exp_excel_file,sheet_name='Final',dtype=str)
aup_excel_file = r"C:\Users\pallist\Desktop\ΤΡΕΧΟΝΤΑ\1) Projects\Suez3\aup merged.xlsx"
aup_mapping_df= pd.read_excel(aup_excel_file,sheet_name='Fin',dtype=str)
df_empty1 = pd.read_excel(exp_excel_file,sheet_name='Final',dtype=str)
df_empty2 = pd.read_excel(exp_excel_file,sheet_name='Final',dtype=str)


# Get total unique cids and total unique loan df
exp_cid_df = pd.read_excel(r"C:\Users\pallist\Desktop\ΤΡΕΧΟΝΤΑ\1) Projects\Suez3\cids laons aup_exposures.xlsx",sheet_name='CID Exposures',dtype='str')
exp_loan_df = pd.read_excel(r"C:\Users\pallist\Desktop\ΤΡΕΧΟΝΤΑ\1) Projects\Suez3\cids laons aup_exposures.xlsx",sheet_name='Loan Exposures',dtype='str')
aup_cid_df = pd.read_excel(r"C:\Users\pallist\Desktop\ΤΡΕΧΟΝΤΑ\1) Projects\Suez3\cids laons aup_exposures.xlsx",sheet_name='CID AUP',dtype='str')
aup_loan_df = pd.read_excel(r"C:\Users\pallist\Desktop\ΤΡΕΧΟΝΤΑ\1) Projects\Suez3\cids laons aup_exposures.xlsx",sheet_name='Loan AUP',dtype='str')

# Unique cids, loan_ids
exp_unique_cids = exp_cid_df.iloc[:,0].to_list()
exp_unique_loan_ids = exp_loan_df.iloc[:,0].to_list()
aup_unique_cids = aup_cid_df.iloc[:,0].to_list()
aup_unique_loan_ids = aup_loan_df.iloc[:,0].to_list()

# Cid columns
all_exp_cid_columns = ['Main CID', 'CID1', 'CID2']
all_aup_cid_columns = ['Main CID', 'CID1', 'CID2']

# Dicts 
dict_names = [
    'main_folders_contents_dict',
    'cid_folders_dict',
    'cid_folders_files_dict',
    'total_files_dict',
    'missing_files_dict',
    # 'max_file_count_per_cid_category'
]
dicts = {f'{prefix}_{name}': {} for prefix in ['aup', 'exp'] for name in dict_names}


total_files_counter = 0
total_pages_counter = 0
