import os
import json
import re
import shutil


def del_sdk_empty_collect(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if file_name.endswith(".json") and file_name.startswith("SDK_Tree"):
                            with open(file_path, encoding='utf-8') as f:
                                data = json.load(f)
                                f.close()
                                if "(0, 0 - " in data["boundsInScreen"]:
                                    if check_bounds_same(data, data["boundsInScreen"]):
                                        match = re.search(r'\((\d+)\)', file_name)
                                        if match:
                                            number = int(match.group(1))
                                            for cfn in os.listdir(sub_folder_path):
                                                cfp = os.path.join(sub_folder_path, cfn)
                                                if str(number) in cfn:
                                                    print("del: " + cfp)
                                                    os.remove(cfp)
                    if len(os.listdir(sub_folder_path)) == 1:
                        shutil.rmtree(sub_folder_path)
                        print("del: " + sub_folder_path)


def check_bounds_same(json_data, bds):
    if isinstance(json_data, dict):
        bounds = json_data["boundsInScreen"]
        if bds == bounds:
            if "children" in json_data:
                children = json_data["children"]
                child_list = []
                for child in children:
                    child_list.append(check_bounds_same(child, bounds))
                return all(child_list)
            else:
                return True
        else:
            return False


folder = './TestCap'
del_sdk_empty_collect(folder)
