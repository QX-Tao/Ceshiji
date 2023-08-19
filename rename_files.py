import os
import re


def rename_file(folder_path):
    files = os.listdir(folder_path)
    file_count = len(files)
    group_count = file_count // 3
    for string in files:
        match = re.search(r'\((\d+)\)', string)
        if match:
            number = int(match.group(1))
            old_name = string
            new_name = old_name.split('(')[0] + "(" + str(number + group_count) + ")" + old_name.split(')')[1]
            os.rename(os.path.join(folder_path, old_name), os.path.join(folder_path, new_name))


def rename_files(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    rename_file(sub_folder_path)


folder = './ConCap'
rename_files(folder)
