import os
import random
import re


def del_access(folder_path):
    print("processing: " + folder_path, end="")
    files = os.listdir(folder_path)
    files_num = []
    for string in files:
        match = re.search(r'无障碍_TreeView\((\d+)\)', string)
        if match:
            number = int(match.group(1))
            files_num.append(number)
    access_keep = random.choice(files_num)
    keep_files = '无障碍_TreeView(' + str(access_keep) + ').json'
    print("          keep: " + keep_files)
    for fn in os.listdir(folder_path):
        fp = os.path.join(folder_path, fn)
        if fn.startswith("无障碍") and fn != keep_files:
            os.remove(fp)
            print("del: " + fp)


def keep_random_access(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    del_access(sub_folder_path)


folder = './TestCap'
keep_random_access(folder)
