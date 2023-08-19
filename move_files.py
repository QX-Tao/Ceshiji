import os
import re
import shutil


def move_file(source_folder, target_folder):
    files = os.listdir(source_folder)
    for file_name in files:
        match = re.search(r'\((\d+)\)', file_name)
        if match:
            source_file_path = os.path.join(source_folder, file_name)
            target_file_path = os.path.join(target_folder, file_name)
            shutil.move(source_file_path, target_file_path)


def move_files(f1, f2):
    fl = os.listdir(f1)
    for i in fl:
        sf1 = os.path.join(f1, i)
        sf2 = os.path.join(f2, i)
        if os.path.isdir(sf1) and os.path.isdir(sf2):
            for fn1, fn2 in zip(os.listdir(sf1), os.listdir(sf2)):
                fp1 = os.path.join(sf1, fn1)
                fp2 = os.path.join(sf2, fn2)
                if os.path.isdir(fp1) and os.path.isdir(fp2):
                    move_file(fp1, fp2)


folder1 = './ConCap'
folder2 = './TestCap'
move_files(folder1, folder2)
