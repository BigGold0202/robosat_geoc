import time
from app.libs import redprint, utils, utils_geom
from flask import jsonify, request
from app.config import setting as SETTING
from robosat_pink.geoc import RSPpredict, RSPreturn_predict
from app.api.v1 import tools as TOOLS, task as TASK, predict_buildings as BUILDINGS, job as JOB
import json

api = redprint.Redprint('predict')


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
        return result

    # 使用robosat_geoc开始预测
    dataPath = SETTING.ROBOSAT_DATA_PATH
    datasetPath = SETTING.ROBOSAT_DATASET_PATH
    ts = time.time()
    dsPredictPath = datasetPath+"/predict_"+str(ts)
    geojson_predcit = RSPpredict.main(
        extent, dataPath, dsPredictPath, map="google")
    if not geojson_predcit:
        result["code"] = 0
        result["msg"] = "预测失败"
        return result

    # 转换为3857坐标系
    geojson3857 = utils_geom.geojson_project(
        geojson_predcit, "epsg:4326", "epsg:3857")

    # geojson 转 shapefile
    shp3857 = dsPredictPath+"/building3857.shp"
    utils_geom.geojson2shp(geojson3857, shp3857)

    # regularize-building-footprint
    # site:https://pro.arcgis.com/zh-cn/pro-app/tool-reference/3d-analyst/regularize-building-footprint.htm
    shp_regularized = dsPredictPath + "/regularized.shp"
    # TODO

    # shp to geojson
    geojson3857 = utils_geom.shp2geojson(shp_regularized)

    # project from 3857 to 4326
    geojson4326 = utils_geom.geojson_project(
        geojson3857, "epsg:3857", "epsg:4326")

    # 给geojson添加properties
    handler = SETTING.IPADDR
    # for feature in geojson4326["features"]:
    for feature in geojson_predcit["features"]:
        feature["properties"] = {
            "task_id": task.task_id,
            "extent": task.extent,
            "user_id": task.user_id,
            "area_code": task.area_code,
            "handler": handler
        }

    # 插入数据库
    result_create = BUILDINGS.insert_buildings(geojson4326)
    if not result_create:
        result["code"] = 0
        result["msg"] = "预测失败"
        return result

    return result
