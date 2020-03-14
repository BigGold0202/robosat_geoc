import os
from flask import jsonify
from app.libs.redprint import Redprint
from app.config import setting as SETTING
api = Redprint('tools')


@api.route('/log', methods=['GET'])
def get_log():
    dataPath = SETTING.ROBOSAT_DATA_PATH
    logPath = dataPath+"/model/log"
    if not os.path.isfile(logPath):
        return "未找到日志文件！，路径为："+logPath
    with open(logPath) as f:
        f = f.readlines()
    logContent = ["这个是日志文件，路径为："+logPath, "", ""]
    for line in f:
        logContent.append("<p>"+line+"</p>")
    logStr = " ".join(logContent)
    return logStr


@api.route('/log/clear', methods=['GET'])
def clear_log():
    dataPath = SETTING.ROBOSAT_DATA_PATH
    logPath = dataPath+"/model/log"
    if not os.path.isfile(logPath):
        return "未找到日志文件！，路径为："+logPath
    open(logPath, "w").close()
    result = {
        "code": 1,
        "msg": "log is clean now."
    }
    return jsonify(result)


def check_extent(extent, train_or_predict, set_maximum=False):
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    if not extent:
        result["code"] = 0
        result["msg"] = "参数有误"
        return result
    coords = extent.split(',')
    if len(coords) != 4:
        result["code"] = 0
        result["msg"] = "参数有误"
        return result
    if "train" in train_or_predict:
        if float(coords[2]) - float(coords[0]) < SETTING.MIN_T_EXTENT or float(coords[3]) - float(coords[1]) < SETTING.MIN_T_EXTENT:
            result["code"] = 0
            result["msg"] = "Extent for training is too small. Training stopped."
    elif "predict" in train_or_predict:
        if float(coords[2]) - float(coords[0]) < SETTING.MIN_P_EXTENT or float(coords[3]) - float(coords[1]) < SETTING.MIN_P_EXTENT:
            result["code"] = 0
            result["msg"] = "Extent for prediction is too small. Predicting stopped."
        elif float(coords[2]) - float(coords[0]) > SETTING.MAX_P_EXTENT or float(coords[3]) - float(coords[1]) > SETTING.MAX_P_EXTENT:
            result["code"] = 0
            result["msg"] = "Extent for prediction is too small. Predicting stopped."
        elif set_maximum and float(coords[2]) - float(coords[0]) > 0.02 or float(coords[3]) - float(coords[1]) > 0.02:
            result["code"] = 0
            result["msg"] = "Extent for prediction is too big. Predicting stopped."
    else:
        result["code"] = 0
        result["msg"] = "got wrong params."
    return result
