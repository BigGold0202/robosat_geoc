from datetime import datetime
import time
import json
from robosat_pink.geoc import RSPtrain, RSPpredict, utils


def train(extent, dataPath, dsPath, epochs=10, map="tdt", auto_delete=False):
    return RSPtrain.main(extent, dataPath, dsPath, epochs, map, auto_delete)


def predict(extent, dataPath, dsPath, map="tdt", auto_delete=False):
    return RSPpredict.main(extent, dataPath, dsPath, map, auto_delete)


if __name__ == "__main__":
    # config.toml & checkpoint.pth data directory
    dataPath = "data"

    # training dataset directory
    startTime = datetime.now()
    ts = time.time()

    # map extent for training or predicting
    #extent = "116.286626640306,39.93972566103653,116.29035683687295,39.942521109411445"
    #extent = "104.7170 31.5125 104.7834 31.4430"#mianyang
    # extent = "116.3094,39.9313,116.3114,39.9323"
    extent = "116.2159,39.7963,116.5240,40.0092"

    result = ""
    # trainging
    result = train(extent, dataPath, "ds/train_" + str(ts), 1)

    # predicting
    #result = predict(extent, dataPath, "ds/predict_" + str(ts))

    print(result)

    endTime = datetime.now()
    timeSpend = (endTime-startTime).seconds
    print("Training or Predicting DONE！All spends：", timeSpend, "seconds！")
