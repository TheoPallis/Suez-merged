# Helper CID Functions
# Imports
import os 
import re
import pandas as pd
from pathlib import Path




elements_list = []

def check_leading_zeroes_cid(cid, unique_cids):
    if cid is not None :
        for i in range(1, 6):
            modified_cid = ('0' * i) + cid
            if modified_cid in unique_cids:
                print(f"Warning!!! The cid {cid} has leading zeroes. It was modified to {modified_cid}")
                # pb.push_note("Warning!!!",f"The cid {cid} has leading zeroes. It was modified to {modified_cid}")
                return modified_cid
    return cid


def add_to_file_dict(cid,files_dict,file_path,unique_cids):
        cid = check_leading_zeroes_cid(cid,unique_cids) 
        if cid.isnumeric() and cid in unique_cids:
            # print(f"Adding {os.path.basename(file_path)} for CID {cid}")
            if cid in files_dict:
                files_dict[cid].append(file_path)
            else:
                files_dict[cid] = [file_path]

def extract_8_digit_part(s):
    match = re.search(r'\b\d{8}\b', s)
    return match.group(0) if match else None



def match_loan_id_to_cid(loan_id,df) :
    cid = df['Main CID'][df['Loan ID'] == loan_id].iloc[0] if not df['Main CID'][df['Loan ID'] == loan_id].empty else "Not Found"
    return cid


def check_for_multiple_loan_cids_for_a_single_loan_id(file_loan_id,df) :
        double_cids = df['Main CID'][df['Loan ID'] == file_loan_id].tolist()
        # Check if a loan id can match to multiple loan cids
        if len(double_cids) > 1:
            print(f"Warning!!! The loan {file_loan_id} has the following multiple loan cids {double_cids}")  

def add_to_file_dict(cid,files_dict,file_path,unique_cids):
        cid = check_leading_zeroes_cid(cid,unique_cids)
        #TODO check why it throws error
        if cid is not None:
            if cid.isnumeric() and cid in unique_cids  :
                # print(f"Adding {os.path.basename(file_path)} for CID {cid}")
                if cid in files_dict:
                    files_dict[cid].append(file_path)
                else:
                    files_dict[cid] = [file_path]

def extract_8_digit_part(s):
    match = re.search(r'\b\d{8}\b', s)
    return match.group(0) if match else None


def get_cid_and_add_files(source,depth,r, file_list,legal_files_dict,unique_cids,df,mode) :
    base_r = os.path.basename(r)       
    for file in file_list :            
        file_path = os.path.join(r, file)
        
        if mode == 'CID Folder' :
            # Get the loan id from the folder name
            if base_r.startswith('0026') and depth == 0:
                mode = 'Loan ID'
                folder_loan_id = base_r
                check_for_multiple_loan_cids_for_a_single_loan_id(folder_loan_id,df)
                cid = match_loan_id_to_cid(folder_loan_id,df)    
            else :
                # Get the top cid folder
                for i in range(7) :
                    if depth  == 0  :
                        cid = extract_8_digit_part(base_r)
                    elif depth == i and depth != 0 :
                        cid_folder = Path(file_path).parents[i]                    
                        cid = os.path.basename(cid_folder)
                        cid = extract_8_digit_part(cid)

        elif mode == 'CID File' :
            base_file = os.path.basename(file)
            cid = extract_8_digit_part(base_file)        
            file_path = os.path.join(r, file)

        if os.path.isfile(file_path):
            elements_list.append({
                'Source' : source,
                'Depth': depth,
                'Cid': cid,
                'Mode': mode,
                'File_path': file_path
                })
            try :
                add_to_file_dict(cid, legal_files_dict, file_path, unique_cids)
            except :
                print(f"{os.path.basename(cid_folder)},Could not add {file_path}")


def process_files(depth,path, r, file_list, dict_in_aup, dict_in_exp, aup_unique_cids,exp_unique_cids, mapping_df, category):
    source = os.path.basename(path)
    get_cid_and_add_files(source,depth,r, file_list, dict_in_aup, aup_unique_cids, mapping_df, category)
    get_cid_and_add_files(source,depth,r, file_list, dict_in_exp, exp_unique_cids, mapping_df, category)

def get_max_files_found_for_each_cid_category(all_cid_columns, max_file_count_per_cid_category, files_dict, df):
    for col in all_cid_columns:
        filtered_files = {k: v for k, v in files_dict.items() if k in df[col].tolist()}
        lengths = [len(v) for v in filtered_files.values() if len(v) > 0] 
        if lengths:
            max_file_count_per_cid_category[col] = max(lengths)
        else:
            max_file_count_per_cid_category[col] = 0
        for i in range(max_file_count_per_cid_category[col]):
            df[f"{col} file {i + 1}"] = df[col].apply(lambda x: files_dict[x][i] if x in files_dict and len(files_dict[x]) > i else '-')
    return df    

def aup_iteration(all_aup_cid_columns,all_exp_cid_columns,aup_max_file_count_per_cid_category,exp_max_file_count_per_cid_category,aup_file_folders_list, aup_legal_files_dict_in_aup, aup_legal_files_dict_in_exp, aup_unique_cids,exp_unique_cids,aup_mapping_df) :
        # Aup iteration
        for path in aup_file_folders_list:
            for r,_, file_list in os.walk(path):
                relative_path = os.path.relpath(r, path)
                depth = relative_path.count(os.sep)
                if r != path:
                    process_files(depth,path, r, file_list, aup_legal_files_dict_in_aup, aup_legal_files_dict_in_exp, aup_unique_cids, exp_unique_cids, aup_mapping_df, 'CID Folder')
                elif r == path :
                    process_files(depth,path, r, file_list, aup_legal_files_dict_in_aup, aup_legal_files_dict_in_exp, aup_unique_cids, exp_unique_cids, aup_mapping_df, 'CID File')
        print("AUP Iteration Done")        

