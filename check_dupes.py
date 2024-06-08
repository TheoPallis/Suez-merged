# Imports
import os 
import re
import hashlib
import pandas as pd
import numpy as np
from collections import defaultdict
import openpyxl
from openpyxl import load_workbook
from openpyxl.styles import Font, Color, PatternFill
from pushbullet  import Pushbullet
from PIL import Image
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError
API = "o.vwm3iRGvehi6jP9PewTb6Wo8ymMYGaxf"


# Helper functions for dupe files and count pages
def count_tiff_pages(file_path):
    with Image.open(file_path) as img:
        total_pages = 0
        try:
            while True:
                img.seek(total_pages)
                total_pages += 1
        except EOFError:
            pass
    return total_pages

def count_pdf_pages(file_path):
    try:
        with open(file_path, "rb") as f:
            if f.read(1):  # Check if the file is not empty
                f.seek(0)  # Reset the file pointer to the beginning
                pdf = PdfReader(f)
                return len(pdf.pages)
            else:
                return 0  # Return 0 if the file is empty
    except PdfReadError as e:
        # print(f"Error reading PDF: {e}")
        return ('25')  # Return 25(approx) to indicate an error


def get_file_hash(file_path):
    hash_func = hashlib.sha256()
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def normalize_basename(filename):
    basename = os.path.basename(filename)
    normalized = re.sub(r'[\s._-]+', '', basename).strip()
    return normalized



def files_are_identical(file_path_1, file_path_2):
    with open(file_path_1, 'rb') as file1, open(file_path_2, 'rb') as file2:
        while True:
            chunk1 = file1.read(8192)
            chunk2 = file2.read(8192)
            if chunk1 != chunk2:
                return False
            if not chunk1:  # End of file
                return True

def get_all_files(directory_path):
    file_paths = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            # print(f"Processing file: {file}")
            file_paths.append(os.path.join(root, file))
    return file_paths

def compare_files_in_directory(directory_path):
    files = get_all_files(directory_path)
    # print("Got all files!")
    file_hashes = {file: get_file_hash(file) for file in files}
    # print("Got all hashes!")
    identical_files = []
    similar_files = []

    for i in range(len(files)):
        # print(f"Comparing file: {files[i]}")
        for j in range(i + 1, len(files)):
            file1 = files[i]
            file2 = files[j]
            if file_hashes[file1] == file_hashes[file2]:
                if files_are_identical(file1, file2):
                    # print(f"  Identical files: {file1} and {file2}")
                    identical_files.append((file1, file2))
            else:
                # Compare files by name and page count if they are not identical
                if normalize_basename(file1) == normalize_basename(file2) and not (normalize_basename(file1).endswith('db')):
                    file1_pages = count_tiff_pages(file1) if file1.lower().endswith('.tiff') else count_pdf_pages(file1)
                    file2_pages = count_tiff_pages(file2) if file2.lower().endswith('.tiff') else count_pdf_pages(file2)
                    if file1_pages == file2_pages:
                        # print(f"  Files with same name and page count: {file1} and {file2}")
                        similar_files.append((file1, file2))
    
    return identical_files, similar_files


# Main dupe file function
directory =  r"\\lawoffice\GSLODocuments\LegalServices_Division\01.Lawoffice_Common\Project Suez 3C\Files AuP\73 Borrowers"

def show_dupe_files(directory, total_files_counter,total_pages_counter,print_mode = 1):

    first_level_subfolders = [os.path.join(directory, name) for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]

    for path in first_level_subfolders:
        seen_files= set()
        identical_files, similar_files = compare_files_in_directory(path)
        if identical_files or similar_files:
            if print_mode in  [1,2] :
                    print(os.path.basename(path))
        if identical_files :
            if print_mode in [1,2]:
                print(" Identical files:")
            for identical_list in identical_files:
                for file in identical_list :
                        if not file.endswith('db') and file not in seen_files:
                            pages =  count_tiff_pages(file) if file.lower().endswith('.tiff') else count_pdf_pages(file)  
                            seen_files.add(file)    
                            total_files_counter += 1
                            if print_mode == 2 :
                                print(f"   Pages : {pages} File : {file}")

        if similar_files :
            if print_mode == 1 :
                print(" Similar files:")
            for similar_list in similar_files:
                for file in similar_list:
                    if not file.endswith('db') and file not in seen_files:
                        pages =  count_tiff_pages(file) if file.lower().endswith('.tiff') else count_pdf_pages(file)  
                        seen_files.add(file)   
                        total_files_counter += 1 
                        if print_mode == 2 :
                            print(f"   Pages : {pages} File : {file}")
    return total_files_counter,total_pages_counter