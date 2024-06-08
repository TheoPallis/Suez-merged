import os
from helper_cid_functions import *
# Get the legal files dict
def get_the_legal_files_exp_dict(file_folders_list,legal_files_dict,unique_cids,df) :
    max_depth = 10
    for path in file_folders_list:
        for r,subfolder_list,file_list in os.walk(path):
            relative_path = os.path.relpath(r, path)
            depth = relative_path.count(os.sep)
            base_r = os.path.basename(r)   
            # Done
            if path == file_folders_list[0]:
                for i in range(max_depth):
                    if depth == i :
                        # print(" "*i,os.path.basename(r))         
                        for file in file_list :
                            # print("\t"*(i+1),os.path.basename(file))
                            file_path = os.path.join(r, file)
                            if os.path.isfile(file_path):
                                file_cid = file.split(" ")[0]
                                add_to_file_dict(file_cid,legal_files_dict,file_path,unique_cids)

            elif path == file_folders_list[1]: 
                # Get the parent name folder
                for i in range(max_depth):
                    if depth == i :
                        # check_subfolders(subfolder_list,legal_files_dict,unique_loan_ids,splitted_dict) :
                        for index,file in enumerate (file_list) :
                            file_path = os.path.join(r, file)
                            if depth == 1 and file_list  :
                                file_loan_id = base_r
                                check_for_multiple_loan_cids_for_a_single_loan_id(file_loan_id,df)                
                                file_cid = match_loan_id_to_cid(file_loan_id,df)
                                if file_path not in legal_files_dict.values() and  file_cid in unique_cids and file_cid != 'Not Found':
                                    # print('\t' * (i+1),"Subfolder", {base_r}, "with CID", {file_cid}, "contains the following files that are not found in the files_dict:")
                                    # print('\t' * (i+2),subfolder_list, {file})
                                    add_to_file_dict(file_cid,legal_files_dict,file_path,unique_cids)

                            elif depth  == 2 and file_list:
                                file_parts = file_path.split(os.sep)
                                cid_or_loan_id_file = file_parts[-3]
                                # WARNING This is not always the case, because some folders may have missing leading zeroes
                                if len(cid_or_loan_id_file) == 8 :
                                    file_cid = cid_or_loan_id_file
                                    add_to_file_dict(file_cid,legal_files_dict,file_path,unique_cids)
                                
                                elif len(cid_or_loan_id_file) != 8 : 
                                    file_loan_id = cid_or_loan_id_file
                                    file_cid = match_loan_id_to_cid(file_loan_id,df)
                                    check_for_multiple_loan_cids_for_a_single_loan_id(file_loan_id,df)   
                                    add_to_file_dict(file_cid,legal_files_dict,file_path,unique_cids)
                            else :
                                print(f"Warning!!! The file {file} in the subfolder {base_r} is not added to the legal_files_dict")

    legal_files_df = get_max_files_found_for_each_cid_category(all_cid_columns,max_file_count_per_cid_category,legal_files_dict,df)
    return legal_files_df,legal_files_dict