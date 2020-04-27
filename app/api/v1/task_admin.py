# import json
from flask import jsonify, request
import json
import collections
from rasterio.warp import transform_bounds
from mercantile import tiles, xy_bounds

from robosat_pink.geojson import geojson_parse_feature
from app.models.base import queryBySQL, db as DB
from app.libs.redprint import Redprint
from app.config import setting as SETTING
from app.models.task_admin import task_admin as TASK_ADMIN


api = Redprint('task_admin')


@api.route('', methods=['GET'])
def create_task_by_areacode():
    result = {
        "code": 1,
        "data": None,
        "msg": "create bat task success！"
    }
    areacode = request.args.get('areacode')
    zoom = request.args.get('zoom') or '14'  # 将区域范围分割成zoom级别瓦片大小的任务
    zoom = eval(zoom)
    
    if not areacode:
        result['code'] = 0
        result['msg'] = "no areacode params"
        return jsonify(result)
    quhuaTable = ''
    if len(areacode) == 9:#FIXME:bug when null areacode
        quhuaTable = SETTING.QUHUA_XIANG
    elif len(areacode) == 6:
        quhuaTable = SETTING.QUHUA_XIAN
    elif len(areacode) == 4:
        quhuaTable = SETTING.QUHUA_SHI
    elif len(areacode) == 2:
        quhuaTable = SETTING.QUHUA_SHENG
    else:
        result['code'] = 0
        result['msg'] = "areacode not support"
        return jsonify(result)

    areacode = areacode.ljust(12, '0')
    sql = """
        SELECT 
        '{{"type": "Feature", "geometry": ' 
        || ST_AsGeoJSON(st_simplify(geom,0.001)) 
        || '}}' AS features 
        FROM {quhuaTable} WHERE code = '{areacode}'
    """
    queryData = queryBySQL(sql.format(
        areacode=areacode, quhuaTable=quhuaTable))
    if not queryData:
        result["code"] = 0
        result["msg"] = "not found this area,areacode:"+areacode
        return jsonify(result)
    area_json = queryData.fetchone()

    feature_map = collections.defaultdict(list)

    # FIXME: fetchall will not always fit in memory...
    for feature in area_json:
        feature_map = geojson_parse_feature(
            zoom, 4326, feature_map, json.loads(feature))

    cover = feature_map.keys()

    extents = []
    for tile in cover:
        w, s, n, e = transform_bounds(
            "epsg:3857", "epsg:4326", *xy_bounds(tile))
        extent = [w, s, n, e]
        extents.append(','.join([str(elem) for elem in extent]))

    for extent in extents:
        # originalExtent = extent
        user_id = "ADMIN"
        area_code = areacode
        with DB.auto_commit():
            task = TASK_ADMIN()
            task.extent = extent
            # task.originalextent = originalExtent
            task.user_id = user_id
            task.area_code = area_code
            DB.session.add(task)

    result['data'] = {
        "count": len(extents),
        "extent": extents
    }
    return jsonify(result)
