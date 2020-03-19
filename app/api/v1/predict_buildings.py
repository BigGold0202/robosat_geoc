from sqlalchemy import or_
from app.models.base import queryBySQL, db as DB
from app.libs.redprint import Redprint
from app.models.predict_buildings import PredictBuildings
from flask import jsonify
from flask import request
from geomet import wkb

import json

api = Redprint('predict_buildings')

#获取任务建筑物
@api.route("", methods=['GET'])
def onegeojson():
    result = {
        "code": 1,
        "data": None,
        "msg": "显示任务图层"
    }
    task_id = request.args.get("task_id")
    if not task_id:
        result["code"] = 0
        result["msg"] = "task_id缺失"
        return jsonify(result)
    sql = '''select st_asgeojson(geom),gid from "BUIA" where gid in (select a.gid from predict_buildings as a where task_id ={task_id}) '''
    sql = '''SELECT jsonb_build_object ( 'type', 'FeatureCollection', 'features', jsonb_agg ( features.feature ) ) 
  FROM (SELECT jsonb_build_object ( 'type', 'Feature', 'id', gid, 'geometry', ST_AsGeoJSON ( geom ) :: jsonb, 'properties', to_jsonb ( inputs ) - 'geom' ) AS feature 
         FROM ( SELECT gid,geom AS geom FROM "predict_buildings" WHERE task_id = {task_id} and status = 1) inputs) features; '''
    queryData = queryBySQL(sql.format(task_id=task_id))
    if not queryData:
        result["code"] = 0
        result["msg"] = "查询语句有问题"
        return jsonify(result)
    row = queryData.fetchone()
<<<<<<< HEAD
    if row['geojson']:
        result["data"] = json.loads(row["geojson"])
    else:
        result['data'] = None
    return jsonify(result)

# 删除建筑物
@api.route('', methods=['DELETE'])
def delete_task(task_id):
    result = {
        "code": 1,
        "data": None,
        "msg": "删除任务成功"
    }
    # check params
    if not task_id.isdigit():
        result["code"] = 0
        result["msg"] = "task_id不是整型"
        return jsonify(result)

    with DB.auto_commit():
        task = TASK.query.filter_by(task_id=task_id).first_or_404()
        task.delete()
        return jsonify(result)
=======
    result["data"] = row[0]

    return jsonify(result)


>>>>>>> a173d195d734dab1c14579df55072741b5dcaded

# @api.route('', methods=['POST'])
# def create_buildings(geojsonObj):
#     result = {
#         "code": 1,
#         "data": None,
#         "msg": "ok"
#     }
#     # check params
#     if request.json:
#         paramsDic = request.json
#         params = json.loads(json.dumps(paramsDic))
#         geojson = params['geojson']
#     else:
#         geojson = geojsonObj

#     buildings = []
#     for feature in geojson["features"]:
#         # featureDump = json.dumps(feature)
#         # newFeat = '{"type":"FeatureCollection","features":['+featureDump+']}'

#         # newFeature = json.loads(newFeat)
#         newBuild = PredictBuildings()
#         newBuild.task_id = feature["properties"]['task_id']
#         newBuild.extent = feature["properties"]['extent']
#         newBuild.user_id = feature["properties"]['user_id']
#         buildings.append(newBuild)

#     # insert into
#     with DB.auto_commit():
#         DB.session.bulk_save_objects(buildings)
#         return jsonify(result)


@api.route('', methods=['POST'])
def update_buildings():
    result = {
        "code": 1,
        "data": None,
        "msg": "建筑物更新成功"
    }
    # check params
    if not request.json:
        result['code'] = 0
        result['msg'] = 'miss params.'
        return jsonify(result)

    paramsDic = request.json
    params = json.loads(json.dumps(paramsDic))

    if 'status' not in params:
        result['code'] = 0
        result['msg'] = 'miss status.'
        return jsonify(result)

    if 'gids' not in params and 'task_id' not in params:
        result['code'] = 0
        result['msg'] = 'miss gids or task_id.'
        return jsonify(result)

    if 'gids' in params and 'task_id' in params:
        result['code'] = 0
        result['msg'] = 'both have gids and task_id.'
        return jsonify(result)

    status = params['status']

    def updateBuildBygids(gids):
        for gid in gids:
            build = PredictBuildings.query.filter_by(gid=gid).first_or_404()
            if not build:
                continue
            build.status = status
            with DB.auto_commit():
                DB.session.add(build)

    if "gids" in params:
        gids = params['gids']
        if not isinstance(gids, list):
            result['code'] = 0
            result['msg'] = 'gids not list type.'
            return jsonify(result)
        updateBuildBygids(gids)

    if "task_id" in params:
        task_id = params['task_id']
        # builds = PredictBuildings.query.filter_by(task_id=task_id)
        # if not builds:
        #     result['code'] = 0
        #     result['msg'] = 'task id not found'
        #     return jsonify(result)
        # for build in builds:
        #     build.status = status
        #     DB.session.bulk_save_objects(builds)
        sql = '''SELECT gid, task_id, extent, user_id, state, status from predict_buildings WHERE task_id = {task_id}'''
        queryData = queryBySQL(sql.format(task_id=task_id))
        if not queryData:
            result["code"] = 0
            result["msg"] = "查询语句有问题"
            return jsonify(result)
        rows = queryData.fetchall()
        gids = []
        for row in rows:
            gid = row.gid
            gids.append(gid)
        updateBuildBygids(gids)
    return jsonify(result)

# @api.route("/<gid>", methods=['GET'])
# def get(gid):
#     result = {
#         "code": 1,
#         "data": None,
#         "msg": "ok"
#     }
#     sql = '''select st_asgeojson(geom),gid as geojson from predict_buildings WHERE gid ={gid}'''
#     queryData = queryBySQL(sql.format(gid=gid))
#     if not queryData:
#         result["code"] = 0
#         result["msg"] = "查询语句有问题"
#         return jsonify(result)
#     if queryData.rowcount == 0:
#         result["code"] = 0
#         result["msg"] = "未查询到内容"
#         return jsonify(result)
#     row = queryData.fetchone()
#     if row['geojson']:
#         result["data"] = json.loads(row["geojson"])
#     else:
#         result['data'] = None
#     return jsonify(result)


# @api.route('', methods=['POST'])
# def create_buildings(geojsonObj):
#     result = {
#         "code": 1,
#         "data": None,
#         "msg": "ok"
#     }
#     # check params
#     if request.json:
#         paramsDic = request.json
#         params = json.loads(json.dumps(paramsDic))
#         geojson = params['geojson']
#     else:
#         geojson = geojsonObj

#     buildings = []
#     for feature in geojson["features"]:
#         # featureDump = json.dumps(feature)
#         # newFeat = '{"type":"FeatureCollection","features":['+featureDump+']}'

#         # newFeature = json.loads(newFeat)
#         newBuild = PredictBuildings()
#         newBuild.task_id = feature["properties"]['task_id']
#         newBuild.extent = feature["properties"]['extent']
#         newBuild.user_id = feature["properties"]['user_id']
#         buildings.append(newBuild)

#     # insert into
#     with DB.auto_commit():
#         DB.session.bulk_save_objects(buildings)
#         return jsonify(result)

def insert_buildings(geojsonObj): # reference: predict.py
    if not geojsonObj:
        return False

    # geojson to buildings array
    buildings = []
    for feature in geojsonObj["features"]:
        geometry = feature['geometry']
        newBuild = PredictBuildings()
        newBuild.task_id = feature["properties"]['task_id']
        newBuild.extent = feature["properties"]['extent']
        newBuild.user_id = feature["properties"]['user_id']
        newBuild.area_code = feature["properties"]['area_code']
        # newBuild.handler = feature["properties"]['handler']
        newBuild.geom = wkb.dumps(geometry).hex()
        buildings.append(newBuild)

    # insert into
    with DB.auto_commit():
        DB.session.bulk_save_objects(buildings)
        return True
