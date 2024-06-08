# Create and move final paths
import os
import shutil


# AUP
def cid_folders_to_final_path(target_directory) :
    # Map the cid target folders in a dict cid : target_folder_path
    target_dict= {}  
    for folder in os.listdir(target_directory): 
        root = os.path.join(target_directory,folder)
        folder_name = os.path.basename(folder)
        target_dict[folder_name] = root
    return target_dict


def create_cid_folders(unique_main_cids):
    main_folders = {}
    for cid in unique_main_cids :
        main_path  = r"\\lawoffice\GSLODocuments\LegalServices_Division\01.Lawoffice_Common\Project Suez 3C\Files AuP\73 Borrowers"
        cid_folder = os.path.join(main_path,cid)
        if  os.path.exists(cid_folder):
            main_folders[cid] = cid_folder
            continue
        else:
            os.makedirs(cid_folder,exist_ok=True)
            main_folders[cid] = cid_folder
    return main_folders


def move_files(unique_legal_files_dict,target_dict) :
#Move files

    for source_cid,source_files in unique_legal_files_dict.items() :
        for target_cid,target_cid_folder_path in target_dict.items() :
            if source_cid == target_cid :
                # print('Cid : %s' % source_cid)
                for source_file in source_files :
                    immediate_parent_folder = os.path.basename(os.path.dirname(source_file))
                    
                    # Get the file name
                    file_name = os.path.basename(source_file)
                    # Create the target path with the immediate parent folder
                    target_file_path = os.path.join(target_cid_folder_path, immediate_parent_folder, file_name)
                    # Create the target directory if it doesn't exist
                    os.makedirs(os.path.dirname(target_file_path), exist_ok=True)
                    
                    # # Move the file
                    if not os.path.exists(target_file_path) :
                    #     shutil.copy2(source_file, target_file_path)
                        print(f"  Moving {os.path.basename(source_file)} to {target_file_path}")
                    else :
                        continue
                        print(f"  File {target_file_path} already exists")
    print("Files moved")