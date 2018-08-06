

import os

current =os.path.dirname(os.path.abspath(__file__))
path =os.path.split(current)[0]

jsonname = "scene.json"
txtname = "scene.txt"
apkname =""

def read_txt():
    """
    读取txtname文件
    :param txtname: str
    :return: filesobj
    """
    txt =path.replace("\\","/")+"/test_files/"+str(txtname)
    return txt


def open_txt():
    """
    读取文件txt
    :return list:
    """
    fd = open(read_txt(),"r",encoding="utf-8")
    while True:
        line = fd.readlines()
        if not line:
            break
        return line
    fd.close()


def open_with_txt():
    """
    with处理读取文件txt
    :return str:
    """
    data =""
    with open(read_txt(),encoding="utf-8") as fd:
        while True:
            line = fd.readlines()
            if not line:
                break
            return data.join(line)

def read_json():
    """
    读取json
    :param jsonname:
    :return:obj
    """
    json =path.replace("\\","/")+"/test_files/"+str(jsonname)
    return json

def open_json(key):
    """
    读取文件
    using:print(open_json(num))
    :param key:int or str
    :return: str
    """
    import json
    with open(read_json(),"r") as fp:
        data = json.load(fp)
        value = data.get(str(key))
        return value


def apk_path():
    """
    读取apk路径
    :return:
    """
    _apk =path.replace("\\","/")+"/test_tools/"+str(apkname)+".apk"
    return _apk



