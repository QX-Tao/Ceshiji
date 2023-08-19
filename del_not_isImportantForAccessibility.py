import os
import json
import re


def merge_nested_json(json_data):
    if isinstance(json_data, dict):
        if "children" in json_data:
            children = json_data["children"]
            merged_list = []
            for child in children:
                if "children" in child and not child["isImportantForAccessibility"]:
                    tmp = merge_nested_json(child)
                    if isinstance(tmp, dict):
                        merged_list.append(tmp)
                    else:
                        for item in tmp:
                            merged_list.append(item)
                elif "children" in child and child["isImportantForAccessibility"]:
                    tmp = merge_nested_json(child)
                    if isinstance(tmp, dict):
                        merged_list.append(tmp)
                    else:
                        for item in tmp:
                            merged_list.append(item)
                elif "children" not in child and child["isImportantForAccessibility"]:
                    merged_list.append(child)
            if json_data["isImportantForAccessibility"]:
                if len(merged_list) == 0:
                    del json_data["children"]
                else:
                    json_data["children"] = merged_list
            else:
                json_data = merged_list
        return json_data


def delete_not_important_views(root_folder):
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
                                merge_nested_json(data)
                                print("processing: " + file_path)
                                f.close()
                            with open(file_path, 'w', encoding="utf-8") as f:
                                json.dump(data, f, ensure_ascii=False, indent=4)
                                f.close()


folder = './TestCap'
delete_not_important_views(folder)
