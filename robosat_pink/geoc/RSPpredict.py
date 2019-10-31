import os
from robosat_pink.tools import cover, download, rasterize, predict, vectorize
import time
import shutil
import json
import multiprocessing

from robosat_pink.geoc import config as CONFIG, params, utils

multiprocessing.set_start_method('spawn', True)


def main(extent, dataPath, dsPath, map="tdt", auto_delete=False):
    # training or predict checkpoint.pth number
    pthNum = utils.getLastPth(dataPath)
    if pthNum == 0:
        return None

    params_cover = params.Cover(
        bbox=extent,
        zoom=18, out=[dsPath + "/cover"])
    cover.main(params_cover)

    params_download = params.Download(
        type="XYZ",
        url=CONFIG.WMTS_HOST+"/{z}/{x}/{y}?type="+map,
        cover=dsPath + "/cover",
        out=dsPath + "/images",
        timeout=20)
    download.main(params_download)

    pthPath = dataPath + "/model/checkpoint-" + \
        str(pthNum).zfill(5)+".pth"

    params_predict = params.Predict(
        dataset=dsPath,
        checkpoint=pthPath,
        config=dataPath+"/config.toml",
        out=dsPath + "/masks"
    )
    predict.main(params_predict)

    params_vectorize = params.Vectorize(
        masks=dsPath + "/masks",
        type="Building",
        config=dataPath+"/config.toml",
        out=dsPath + "/vectors.json"
    )
    vectorize.main(params_vectorize)

    params_features = params.Features(
        masks=dsPath + "/masks",
        type="parking",
        dataset=dataPath+"/config.toml",
        out=dsPath + "/features.json"
    )
    features.main(params_features)
    
    # 解析预测结果并返回
    jsonFile = open(dsPath + "/vectors.json", 'r')
    jsonObj = json.load(jsonFile)

    # if auto_delete:
    #     shutil.rmtree(dsPath)

    return jsonObj


    # 解析预测结果并返回
    jsonFile = open(dsPath + "/features.json", 'r')
    jsonObj = json.load(jsonFile)




    params_merge = params.Merge(
        features=dsPath + "/features.json",
        threshold=1,
        out=dsPath + "/merged_features.json"
    )
    merge.main(params_merge)


    # 解析预测结果并返回
    jsonFile = open(dsPath + "/merged_features.json", 'r')
    jsonObj = json.load(jsonFile)

    if auto_delete:
        shutil.rmtree(dsPath)

    return jsonObj