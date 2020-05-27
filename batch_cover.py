from datetime import datetime
import time
import json
from robosat_pink.geoc import RSPcover, utils
from app.libs import utils_geom

def cover(dsPath,geojson,out):
    return RSPcover.main(dsPath,geojson,out)

if __name__ == "__main__":
    # # if cover by dir
    # dsPath = "/data/dataset/train/train_2/tdttianjin/training/labels"
    # geojson = None
    # out = None

    # if cover by geojson
    dsPath = None
    dir = '/data/dataset/train/train_3_0527'
    # jsonFile = open(dir + "/centroid_buffer_union.json", 'r')
    geojson = dir + "/centroid_buffer_union.json"
    out = [dir+'/cover']

    # training dataset directory
    startTime = datetime.now()
    ts = time.time()

    result = cover(dsPath,geojson,out)

    endTime = datetime.now()
    timeSpend = (endTime-startTime).seconds
    print("Cover DONE！All spends：", timeSpend, "seconds！")
