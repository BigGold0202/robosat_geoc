#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask, request
import os
import subprocess
import setting as SETTING


app = Flask(__name__)

current_path = os.path.abspath(os.getcwd())

command_path = current_path + "/" + SETTING.COMMAND_FILE
config_path = SETTING.CONFIG_PATH_TXT


@app.route('/')
def hello_world():
    return 'Hello flask!'


@app.route('/regularize', methods=['GET'])
def wmts():
    print("start flask")
    result = {
        "code": 1,
        "data": None,
        "msg": "ok"
    }
    path = request.args.get("path")
    with open(config_path, 'w') as f:
        f.write(path)
        f.close()
    # FNULL = open(os.devnull, 'w')
    try:
        proc = subprocess.check_output(
            [SETTING.CONFIG_ARCPY, command_path], stderr=subprocess.STDOUT)
    except subprocess.CalledProcessError:
        print(subprocess.STDOUT)
    print(proc)
    if not proc or "Failed" in proc:
        result['code'] = 0
        result['msg'] = 'execute arcpy command failed.'
    if "regularized.shp already exists" in proc:
        result['code'] = 1
        result['msg'] = 'regularized.shp already exists.'
    return result


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
