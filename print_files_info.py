import os
import re
import sys
from colorama import Fore, Style


def print_file_info(folder_path):
    print("loc: " + folder_path)
    files = os.listdir(folder_path)
    files_num = []
    for string in files:
        match = re.search(r'SDK_TreeView\((\d+)\)', string)
        if match:
            number = int(match.group(1))
            files_num.append(number)
    for i in files_num:
        sdk_files_name = 'SDK_TreeView(' + str(i) + ').json'
        sdk_files_size = os.path.getsize(os.path.join(folder_path, sdk_files_name))
        access_files_name = '无障碍_TreeView(' + str(i) + ').json'
        access_files_size = os.path.getsize(os.path.join(folder_path, access_files_name))
        print(Fore.GREEN + str(i) + ":   " +
              str(sdk_files_size) + "B (" + str(bytes_to_kilobytes(sdk_files_size)) + "KB)" + "   " +
              str(access_files_size) + "B (" + str(bytes_to_kilobytes(access_files_size)) + "KB)" + "   " +
              str(abs(sdk_files_size - access_files_size)) + "B (" +
              str(bytes_to_kilobytes(abs(sdk_files_size - access_files_size))) + "KB)" + Style.RESET_ALL, end='   ')
        threshold = (access_files_size + sdk_files_size) // 25
        if abs(sdk_files_size - access_files_size) > threshold:
            print(Fore.RED + "unexpected!" + Style.RESET_ALL)
        else:
            # clear_line()
            print()


def clear_line():
    sys.stdout.write("\r")
    sys.stdout.write(" " * 80)
    sys.stdout.write("\r")
    sys.stdout.flush()


def bytes_to_kilobytes(file_bytes):
    kilobytes = file_bytes / 1024
    return "{:.2f}".format(kilobytes)


def print_files_info(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    print_file_info(sub_folder_path)


folder = './PreCap'
print_files_info(folder)
