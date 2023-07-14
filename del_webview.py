import os
import json
import shutil


def delete_folders_with_delete_field(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if file_name.endswith(".json"):
                            with open(file_path, encoding='utf-8') as f:
                                data = json.load(f)
                                tmp = json.dumps(data)
                                f.close()
                                if "wvDom" in tmp:
                                    # 删除外层文件夹
                                    shutil.rmtree(sub_folder_path)
                                    break


folder = './CaptureInterface'
delete_folders_with_delete_field(folder)
