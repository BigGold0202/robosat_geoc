import os
import arcpy
import time
import setting as SETTING

print("start load arcpy")
startTime = time.clock()


arcpy.env.workspace = SETTING.DATA_PATH

config_path = SETTING.DATA_PATH + "config.txt"

with open(config_path, 'r') as f:
    lines = f.readlines()
    path = lines[0].strip()


def reguar():
    print("start regularize")
    try:
        DIR_PATH = SETTING.DATA_PATH + path
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
    endTime = time.clock()

    print("end regular")
    print ("spendssss:" + str(endTime-startTime))


if __name__ == "__main__":
    reguar()
