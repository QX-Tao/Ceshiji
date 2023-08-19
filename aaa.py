#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import json


def simplify_class(class_name):
    words = class_name.split('.')
    simplified = ''
    for word in words:
        if word and word[0].islower():
            simplified += word[0]
        elif word:
            simplified += ''.join(char for char in word if char.isupper())
    return simplified


def encode_node(node, level, parent_class=""):
    class_name = node.get("class", "")
    if not class_name:
        return ()

    simplified_class = simplify_class(class_name)
    simplified_parent_class = simplify_class(parent_class)

    encoded = f"{level}{simplified_class}{simplified_parent_class}"
    children = node.get("children", [])
    result = [encoded]
    for child in children:
        child_result = encode_node(child, level + 1, class_name)
        result.extend(child_result)
    return tuple(result)


def encode_control_tree(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        control_tree = json.load(file)
    return encode_node(control_tree, 1)


def calculate_similarity(tuple1, tuple2):
    common_elements = []
    for element in tuple1:
        if element in tuple2:
            common_elements.append(element)
            tuple2.remove(element)  # 从tuple2中移除已匹配的元素
    max_elements = max(len(tuple1), len(tuple2) + len(common_elements))  # 考虑tuple2中剩余的元素和已匹配的元素
    similarity = len(common_elements) / max_elements
    return similarity


def compare_files(sdk_files, acc_files):
    correct_count = 0
    total_count = 0

    for sdk_file in sdk_files:
        sdk_folder = os.path.dirname(sdk_file)
        parent_folder = os.path.basename(os.path.dirname(sdk_folder))

        sdk_folder_first_file = os.listdir(sdk_folder)[0]

        max_similarity = 0.0
        max_acc_file = ""

        for acc_file in acc_files:
            acc_folder = os.path.dirname(acc_file)
            acc_folder_first_file = os.listdir(acc_folder)[0]

            if sdk_folder_first_file != acc_folder_first_file:
                continue

            result1 = encode_control_tree(sdk_file)
            result2 = encode_control_tree(acc_file)

            similarity = calculate_similarity(list(result1), list(result2))

            if similarity > max_similarity:
                max_similarity = similarity
                max_acc_file = acc_file

        print("SDK 文件:", sdk_file)
        print("最相似的无障碍文件:", max_acc_file)
        print("相似度:", max_similarity)

        # 提取文件夹路径
        sdk_folder_path = os.path.dirname(sdk_file)
        max_acc_folder_path = os.path.dirname(max_acc_file)

        if sdk_folder_path == max_acc_folder_path:
            # print("计算正确")
            correct_count += 1
        else:
            # print("计算错误")
            pass
            # print("======================")
        total_count += 1

    accuracy = correct_count / total_count

    print("APP: {:35} 准确度: {:.8f}".format(parent_folder, accuracy))
    # print("准确度:", accuracy)


def process_files_in_folder(folder_path):
    sdk_files = []
    acc_files = []

    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.startswith("SDK_TreeView") and file.endswith(".json"):
                sdk_files.append(os.path.join(root, file))
            elif file.startswith("无障碍_TreeView") and file.endswith(".json"):
                acc_files.append(os.path.join(root, file))

    compare_files(sdk_files, acc_files)


# 输入根目录路径
root_dir = r".\TestCap"

for folder_name in os.listdir(root_dir):
    folder_path = os.path.join(root_dir, folder_name)
    if os.path.isdir(folder_path):
        process_files_in_folder(folder_path)

