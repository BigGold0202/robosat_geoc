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
    path = request.args.get("path")
    with open(config_path, 'w') as f:
        f.write(path)
        f.close()
    p = subprocess.call([SETTING.CONFIG_ARCPY, command_path])
    print(p)
    return "ok"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
