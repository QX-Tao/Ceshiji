import os
import json
import re
import shutil


def del_sdk_empty_and_error_collect(root_folder):
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
                                try:
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
                                except json.decoder.JSONDecodeError:
                                    f.close()
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


def delete_folders_with_delete_field(root_folder):
    for folder_name in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            for sub_folder_name in os.listdir(folder_path):
                sub_folder_path = os.path.join(folder_path, sub_folder_name)
                if os.path.isdir(sub_folder_path):
                    for file_name in os.listdir(sub_folder_path):
                        file_path = os.path.join(sub_folder_path, file_name)
                        if file_name.startswith("Activity_"):
                            if any(activity in file_name for activity in delete_activity):
                                shutil.rmtree(sub_folder_path)
                                print("del: " + sub_folder_path)
                                break
                        if file_name.endswith(".json"):
                            with open(file_path, encoding='utf-8') as f:
                                data = json.load(f)
                                tmp = json.dumps(data)
                                f.close()
                                if any(field in tmp for field in delete_fields):
                                    shutil.rmtree(sub_folder_path)
                                    print("del: " + sub_folder_path)
                                    break


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
delete_fields = ["wvDom",
                 "LynxFlattenUI",
                 "com.uc.webview.export.WebView",
                 "android.webkit.WebView"
                 ]
delete_activity = ["com.taobao.weex.weexv2.page.WeexV2Activity",
                   "com.douban.frodo.flutter.FRDFlutterActivity",
                   "me.ele.component.webcontainer.view.AppUCWebActivity",
                   "com.shizhuang.duapp.modules.web.ui.BrowserActivity",
                   "tv.danmaku.bili.ui.webview.MWebActivity",
                   "com.jd.lib.jdflutter.JDFlutterMainActivity"
                   ]
del_sdk_empty_and_error_collect(folder)
delete_folders_with_delete_field(folder)
delete_not_important_views(folder)
