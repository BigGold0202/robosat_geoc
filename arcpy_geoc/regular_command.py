import os
import arcpy
import time
import setting as SETTING

print("start load arcpy")
startTime = time.clock()


arcpy.env.workspace = SETTING.DATA_PATH

envTime = time.clock()
print("envTime:" + str(envTime-startTime))


config_path = SETTING.DATA_PATH + "config.txt"

with open(config_path, 'r') as f:
    lines = f.readlines()
    path = lines[0].strip()


def reguar():
    # print("start regularize")
    try:
        DIR_PATH = SETTING.DATA_PATH + path
        building1_path = os.path.join(DIR_PATH, 'building1_predict.shp')
        building2_path = os.path.join(DIR_PATH, 'building2_3857.shp')
        building3_path = os.path.join(DIR_PATH, 'building3_merged.shp')
        building4_path = os.path.join(DIR_PATH, 'building4_regularized.shp')
        building5_path = os.path.join(DIR_PATH, 'building5_4326.shp')

        # project
        WKT4326 = 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'
        WKT3857 = 'PROJCS["WGS_1984_Web_Mercator_Auxiliary_Sphere",GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]],PROJECTION["Mercator_Auxiliary_Sphere"],PARAMETER["False_Easting",0.0],PARAMETER["False_Northing",0.0],PARAMETER["Central_Meridian",0.0],PARAMETER["Standard_Parallel_1",0.0],PARAMETER["Auxiliary_Sphere_Type",0.0],UNIT["Meter",1.0]]'
        CS4326 = arcpy.SpatialReference()
        CS3857 = arcpy.SpatialReference()
        CS4326.loadFromString(WKT4326)
        CS3857.loadFromString(WKT3857)

        # project
        print("1.start project")
        arcpy.Project_management(
            building1_path, building2_path, CS3857, "", CS4326)

        print("2.start merge")
        # merge
        arcpy.Dissolve_management(building2_path, building3_path,
                                  "", "", "",
                                  "DISSOLVE_LINES")
        print("3.start regularize")
        # regularize
        arcpy.ddd.RegularizeBuildingFootprint(building3_path,
                                              building4_path,
                                              method='RIGHT_ANGLES',
                                              tolerance=10,
                                              precision=0.25,
                                              min_radius=0.1,
                                              max_radius=1000000)
        # unpreject
        print("4.start unproject")
        arcpy.Project_management(
            building4_path, building5_path, CS4326, "", CS3857)
    except arcpy.ExecuteError:
        print(arcpy.GetMessages())

    endTime = time.clock()
    print("end regular")
    print("spendssss:" + str(endTime-startTime))
    print("okka")
    return "okkkb"


if __name__ == "__main__":
    reguar()
