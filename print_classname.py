import os
import json
from colorama import Fore, Style

aa = []
file_path = ""


def print_classname(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        global file_path
                        file_path = os.path.join(sub_folder_path, file_name)
                        if file_name.endswith(".json"):
                            with open(file_path, encoding='utf-8') as f:
                                data = json.load(f)
                                print_class(data)
                                f.close()


def print_class(json_obj):
    if isinstance(json_obj, dict):
        if "class" in json_obj:
            add_unique_element(json_obj["class"])
        if "children" in json_obj:
            print_class(json_obj["children"])
    elif isinstance(json_obj, list):
        for item in json_obj:
            print_class(item)


def add_unique_element(element):
    if element not in aa:  # 检查元素是否已经存在于列表中
        aa.append(element)  # 添加元素到列表中
        print(element + "  " + Fore.RED + file_path + Style.RESET_ALL)


folder = './CaptureInterface'
print_classname(folder)
