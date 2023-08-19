import os
import json
import re


def delete_node(json_obj, key, value):
    if isinstance(json_obj, dict):
        if key in json_obj and json_obj[key] == value:
            return None
        else:
            for k, v in list(json_obj.items()):
                json_obj[k] = delete_node(v, key, value)
                if json_obj[k] is None:
                    del json_obj[k]
    elif isinstance(json_obj, list):
        json_obj = [delete_node(item, key, value) for item in json_obj]
        json_obj = [item for item in json_obj if item is not None]
    return json_obj


def delete_visible8(root_folder):
    pattern = r'^SDK_TreeView\(\d+\)\.json$'
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if re.match(pattern, file_name):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                data = delete_node(data, 'visible', 8)
                                print("processing: " + file_path)
                                f.close()
                            with open(file_path, 'w', encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False)
                                f.close()


def delete_visible4(root_folder):
    pattern = r'^SDK_TreeView\(\d+\)\.json$'
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if re.match(pattern, file_name):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                data = delete_node(data, 'visible', 4)
                                print("processing: " + file_path)
                                f.close()
                            with open(file_path, 'w', encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False)
                                f.close()


folder = './CaptureInterface'
delete_visible8(folder)
delete_visible4(folder)
