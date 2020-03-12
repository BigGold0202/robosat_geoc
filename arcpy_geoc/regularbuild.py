import arcpy
import requests
from flask import Flask, request, Response
import jsonify
import json
import os
app = Flask(__name__)

DATA_PATH = 'C:/Users/wucan/Documents/data'


@app.route('/')
def hello_world():
    return 'Hello flask!'


@app.route('/v1/regularize', methods=['POST'])
def wmts():
    result = {
        "code": 1,
        "data": None,
        "msg": "修改或创建成功！"
    }

    # geojsonStr = request.form.get('geojson')
    # geojsonStr = eval("'{}'".format(geojsonStr))
    jsonPath = DATA_PATH + '/data.json'
    # with open(jsonPath, 'w') as outfile:
    #     outfile.write(geojsonStr)
    #     outfile.close()
    # return jsonify(result)

    try:
        arcpy.JSONToFeatures_conversion(
            jsonPath, os.path.join(DATA_PATH, "outgdb.gdb", "buildings"))
    #     arcpy.ddd.RegularizeBuildingFootprint('buildings.shp',
    #                                           'regularized_footprints.shp',
    #                                           method='RIGHT_ANGLES',
    #                                           tolerance=10,
    #                                           precision=0.25,
    #                                           min_radius=0.1,
    #                                           max_radius=1000000)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
    print "ok"
    return "ok"


if __name__ == '__main__':
    arcpy.env.workspace = DATA_PATH
    app.run(port=5001)

# if __name__ == "__main__":
#     wmts()
