import os
import json
import re


def remove_unnecessary_keys(json_obj, keys_list):
    if isinstance(json_obj, dict):
        for key in list(json_obj.keys()):
            if key in keys_list:
                del json_obj[key]
            else:
                remove_unnecessary_keys(json_obj[key], keys_list)
    elif isinstance(json_obj, list):
        for item in json_obj:
            remove_unnecessary_keys(item, keys_list)


def delete_unnecessary_field(root_folder):
    pattern1 = r'^SDK_TreeView\(\d+\)\.json$'
    pattern2 = r'^无障碍_TreeView\(\d+\)\.json$'
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if re.match(pattern1, file_name) or re.match(pattern2, file_name):
                            with open(file_path, 'r', encoding='utf-8') as f:
                                data = json.load(f)
                                remove_unnecessary_keys(data, keys_to_remove)
                                print("processing: " + file_path)
                                f.close()
                            with open(file_path, 'w', encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                f.close()


folder = './TestCap'
keys_to_remove = ["isImportantForAccessibility", "isFocused", "isVisibleToUser", "isSelected", "isEnabled",
                  "boundsInScreen", "text", "contentDescription", "resourceId"]  # 要删除的键列表
delete_unnecessary_field(folder)
