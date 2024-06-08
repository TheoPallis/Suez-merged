import pandas as pd
import os
from helper_cid_functions import *
# Get the legal files found in loan/cid files folders of each cid and Get the FOLDERS (loan/cid files) of each cid
# Mapping Df
def get_exp_loan_files(unique_cids):
    cid_folders_files_dict = {}
    # Depths are ok
    from concurrent.futures import ThreadPoolExecutor,as_completed
    base_path = r"\\lawoffice\GSLODocuments\LegalServices_Division\01.Lawoffice_Common\Project Suez 3C\Files\Loan Files"
    zero_depth = ['15-05-24','20-05-24','22-05-24'] 
    single_depth = ['08-05-24','09-05-24'] 
    double_depth = ['10-05-24','13-05-24'] 

    depth_dict = {
        0: zero_depth,
        1: single_depth,
        2: double_depth
    }

    cid_folder_paths = []

    def list_first_level_folders(base_path):
        with os.scandir(base_path) as entries:
            for entry in entries:
                if entry.is_dir() and entry.name != 'Legal docs':
                    cid_folder_paths.append(entry.path)
    list_first_level_folders(base_path)

    for path in cid_folder_paths:
            # pb.push_note('Status',f"Processing {os.path.basename(path)}")
            for root, _, files in os.walk(path):
                folder = os.path.basename(root)
                print(folder)
                rel_path = os.path.relpath(root, path)
                depth = rel_path.count(os.sep)

                if depth < max_depth:
                    depth_list = depth_dict.get(depth, [])
                    if any(date in root for date in depth_list):
                        # add_to_file_dict(folder, cid_folders_dict, root, unique_cids)
                        indent = " " * (depth + 1)
                    else:
                        indent = " " * (depth + (depth - 1))
                    # print(indent + folder)
                    for file in files:
                        # print(indent, folder, file)
                        file_path = os.path.join(root, file)
                        print(root,folder,file_path)
                        add_to_file_dict(folder,cid_folders_files_dict, file_path, unique_cids)
    legal_files_df = get_max_files_found_for_each_cid_category(all_cid_columns,max_file_count_per_cid_category,legal_files_dict,df)

    return legal_files_df,cid_folders_files_dict

