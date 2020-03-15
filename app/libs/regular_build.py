#!/usr/bin/env python
# -*- coding: utf-8 -*-
import arcpy
from flask import Flask, request, Response
import os
import time

app = Flask(__name__)

DATA_PATH = "Z:/"


@app.route('/')
def hello_world():
    return 'Hello flask!'


@app.route('/regularize', methods=['GET'])
def wmts():
    # result = {
    #     "code": 1,
    #     "data": None,
    #     "msg": "修改或创建成功！"
    # }
    path = request.args.get("path")
    # path = "predict_1584276596.093185"
    print("path:"+path)
    if not path:
        return False

    startTime = time.clock()
    print("start regular")
    try:
        DIR_PATH = DATA_PATH + path
        org_path = os.path.join(DIR_PATH, 'building3857.shp')
        regular_path = os.path.join(
            DIR_PATH, 'regularized.shp')
        arcpy.ddd.RegularizeBuildingFootprint(org_path,
                                              regular_path,
                                              method='RIGHT_ANGLES',
                                              tolerance=10,
                                              precision=0.25,
                                              min_radius=0.1,
                                              max_radius=1000000)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())
        return False
    endTime = time.clock()

    print("end regular")
    print ("spendssss:", endTime-startTime)
    return True


if __name__ == '__main__':
    arcpy.env.workspace = DATA_PATH
    app.run(host='0.0.0.0', port=5001, debug=True)

# if __name__ == "__main__":
#     wmts()
