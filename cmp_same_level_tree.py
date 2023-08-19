import json
import os

# 生成递减序列
def generate_exponential_decreasing_sequence(n, base):
    sequence = [1] * 1
    for i in range(7, n):
        sequence.append(sequence[-1] * base)
    return [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]


# 设置要生成的项数和底数
num_items = 50
exp_base = 1.1

# 生成权值序列
weight_sequence = generate_exponential_decreasing_sequence(num_items, exp_base)

def build_tree(json_data):
    node = {
        "class": "",
        "children": []
    }
    if "class" in json_data:
        node["class"] = json_data["class"]
    if "children" in json_data:
        for child_data in json_data["children"]:
            child_node = build_tree(child_data)
            node["children"].append(child_node)
    return node


def bfs_collect_classes(json_tree):
    result = []
    if not json_tree:
        return result

    queue = [(json_tree, 0)]

    while queue:
        current_level_nodes = []
        next_level = []

        while queue:
            node, level = queue.pop(0)
            if 'class' in node:
                current_level_nodes.append(node['class'])

            if 'children' in node:
                for child in node['children']:
                    next_level.append((child, level + 1))

        queue = next_level
        result.append(current_level_nodes)

    return result

def compare_json_trees(tree1, tree2):
    classes1 = bfs_collect_classes(tree1)
    classes2 = bfs_collect_classes(tree2)

    num_diff = 0
    for level, class_list1 in enumerate(classes1):
        if level >= len(classes2):
            num_diff += len(class_list1) * weight_sequence[level]
        else:
            class_list2 = classes2[level]
            class_count1 = {class_name: class_list1.count(class_name) for class_name in class_list1}
            class_count2 = {class_name: class_list2.count(class_name) for class_name in class_list2}
            for class_name in set(class_list1 + class_list2):
                num_diff += abs(class_count1.get(class_name, 0) - class_count2.get(class_name, 0)) * weight_sequence[level]

    num_diff += sum(len(class_list) * weight_sequence[level] for level, class_list in enumerate(classes2[len(classes1):]))

    return num_diff

# 批处理其中的 SDK_TreeView.json 文件
def SDK_batch_process_json_files(directory):

    # 存储文件路径和控件树数据的列表
    json_with_trees_activitys = []

    for filepath in os.listdir(directory):
        #print(filepath)
        activity_name = ""
        for filename in os.listdir(os.path.join(directory, filepath)):
            if filename.startswith("Activity"):
                activity_name = filename
                break
        if activity_name is not None:
            for filename in os.listdir(directory+"\\"+filepath):
                if filename.startswith("SDK"):
                    file_path = os.path.join(directory+"\\"+filepath, filename)
                    #print(file_path)
                    # 读取JSON数据
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)

                    # 构建树结构
                    tree = build_tree(json_data)

                    # 将文件路径和控件树数据添加到列表中
                    json_with_trees_activitys.append((filepath, tree, activity_name,filename))
    #print(json_with_trees_activitys)
    return json_with_trees_activitys

# 批处理其中的 无障碍_TreeView.json 文件
def Free_batch_process_json_files(directory):

    # 存储文件路径和控件树数据的列表
    json_with_trees_activitys = []

    for filepath in os.listdir(directory):
        # print(filepath)
        activity_name = ""
        for filename in os.listdir(os.path.join(directory, filepath)):
            if filename.startswith("Activity"):
                activity_name = filename
                break
        if activity_name is not None:
            id = 0
            for filename in os.listdir(directory + "\\" + filepath):
                if filename.startswith("无障碍"):
                    file_path = os.path.join(directory + "\\" + filepath, filename)
                    # print(file_path)
                    # 读取JSON数据
                    with open(file_path, 'r', encoding='utf-8') as json_file:
                        json_data = json.load(json_file)

                    # 构建树结构
                    tree = build_tree(json_data)

                    # 将文件路径和控件树数据添加到列表中
                    json_with_trees_activitys.append((filepath, tree, activity_name, filename))
                    id+=1
                    if id == 1:
                        break
    # print(json_with_trees_activitys)
    return json_with_trees_activitys


if __name__ == "__main__":

    print(weight_sequence)
    ss = 0

    app_lists = ['cn.kuwo.player']

    Aver_acc = 0

    for app_name in app_lists:
        json_files_directory = './TestCap/' + app_name

        SDK_json_tree_activity = SDK_batch_process_json_files(json_files_directory)
        Free_json_tree_activity = Free_batch_process_json_files(json_files_directory)

        total_sum = len(SDK_json_tree_activity)
        #print(len(Free_json_tree_activity))
        acc = 0

        for index1, info1 in enumerate(SDK_json_tree_activity):
            filepath1 = info1[0]
            tree1 = info1[1]
            activity1 = info1[2]
            sdk_name = info1[3]
            min_distance = 99999
            answer = ""

            for index2, info2 in enumerate(Free_json_tree_activity):
                filepath2 = info2[0]
                tree2 = info2[1]
                activity2 = info2[2]

                if activity1 == activity2:
                    global_distance = compare_json_trees(tree1,tree2)

                    #print(filepath2 + "  " + str(global_distance))
                    if min_distance > global_distance:
                        min_distance = global_distance
                        answer = filepath2

            if answer == filepath1:
                acc+=1
            else:
                print(filepath1 + " " + sdk_name + "   " + answer + "   Min_distance is " + str(min_distance))


        print("The Accuracy of " + app_name + ": " + str(acc/total_sum))
        Aver_acc += acc/total_sum
        #print(weight_sequence)
    print("Average Accuracy: " + str(Aver_acc/77))