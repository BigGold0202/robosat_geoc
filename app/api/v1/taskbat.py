# import json
from flask import jsonify, request
from app.models.base import queryBySQL, db as DB
# from app.models.task import task as TASK
from app.libs.redprint import Redprint
# from app.config import setting as SETTING
# from app.api.v1 import tools as TOOLS
from robosat_pink.geojson import geojson_parse_feature
import json
from rasterio.warp import transform_bounds
# import time
# import sys
import collections
from mercantile import tiles, xy_bounds

api = Redprint('taskbat')


@api.route('', methods=['GET'])
def create_task_by_areacode():
    result = {
        "code": 1,
        "data": None,
        "msg": "create bat task success！"
    }
    areacode = request.args.get('areacode')
    zoom = request.args.get('zoom') or 14

    if areacode:
        sql = """
             SELECT 
               '{{"type": "Feature", "geometry": ' 
               || ST_AsGeoJSON(st_simplify(geom,0.001)) 
               || '}}' AS features 
             FROM quhua_xian WHERE code = '{areacode}'
            """
        queryData = queryBySQL(sql.format(areacode=areacode))
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

    _cover = []
    extent_w, extent_s, extent_n, extent_e = (180.0, 90.0, -180.0, -90.0)
    for tile in cover:
        w, s, n, e = transform_bounds(
            "epsg:3857", "epsg:4326", *xy_bounds(tile))
        _cover.append(tile)

    cover = _cover

    result['data'] = cover
    return jsonify(result)


# if __name__ == "__main__":
#     areacode = '110108'
#     create_task_by_areacode(areacode)
#     pass
