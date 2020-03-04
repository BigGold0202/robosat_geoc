import time
from app.libs.redprint import Redprint
from flask import jsonify, request
from app.config import setting as SETTING
from robosat_pink.geoc import RSPpredict, RSPreturn_predict
from app.api.v1 import tools as TOOLS, task as TASK, predict_buildings as BUILDINGS, job as JOB
import json

api = Redprint('predict')


@api.route('', methods=['GET'])
def predict():
    # check extent
    extent = request.args.get("extent")
    result = TOOLS.check_extent(extent, "predict", True)
    # result = TOOLS.check_extent(extent, "predict")
    if result["code"] == 0:
        return jsonify(result)

    # 使用robosat_geoc开始预测
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()

    dsPredictPath = datasetPath+"/predict_"+str(ts)
    geojson = RSPpredict.main(
        # extent, dataPath, dsPredictPath, map="tdt")
        extent, dataPath, dsPredictPath, map="google")

    # dsPredictPath = datasetPath+"/return_predict_"+str(ts)
    # geojson = RSPreturn_predict.main(
    #     extent
    #     )

    if not geojson:
        result["code"] = 0
        result["msg"] = "预测失败"
        return jsonify(result)
    # 给geojson添加properties
    for feature in geojson["features"]:
        feature["properties"] = {}

    result["data"] = geojson
    return jsonify(result)


def predict_job(task):
    extent = task.extent
    result = TOOLS.check_extent(extent, "predict", True)
    if result["code"] == 0:
        return jsonify(result)

    # 使用robosat_geoc开始预测
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()
    dsPredictPath = datasetPath+"/predict_"+str(ts)
    geojson = RSPpredict.main(
        extent, dataPath, dsPredictPath, map="google")

    if not geojson:
        result["code"] = 0
        result["msg"] = "预测失败"
        return result
    # 给geojson添加properties
    for feature in geojson["features"]:
        feature["properties"] = {
            "task_id": task.task_id,
            "extent": task.extent,
            "user_id": task.user_id
        }

    # 插入数据库
    result_create = BUILDINGS.insert_buildings(geojson)
    if not result_create:
        result["code"] = 0
        result["msg"] = "预测失败"
        return result

    return result
