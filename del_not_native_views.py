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
delete_folders_with_delete_field(folder)
