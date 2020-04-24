from app.libs import utils as UTILS

# building outline PostGIS data table using by training label
BUILDINGS_TABLE = "BUIA"

# USER OR ADMIN MODE
USER_OR_ADMIN = "USER"
# USER_OR_ADMIN = "admin"

QUHUA_SHENG = "data_1741"
QUHUA_SHI = "data_1745"
QUHUA_XIAN = "data_1746"
QUHUA_XIANG = "data_1744"

ARCPY_HOST = "http://172.16.105.70:5001/regularize?path={path}"
# ARCPY_HOST = "http://localhost:5001/regularize?path={path}"

# config.toml and checkpoint.pth files path
ROBOSAT_DATA_PATH = "/data/datamodel"
# ROBOSAT_DATA_PATH = "data"

# dataset to training or predicting
ROBOSAT_DATASET_PATH = "/data/dataset"
# ROBOSAT_DATASET_PATH = "dataset"
# ROBOSAT_DATASET_PATH = "/mnt/c/Users/WUCAN/Documents/dataset"


# tianditu and google map remote sensing wmts url
URL_TDT = '''https://t1.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=4830425f5d789b48b967b1062deb8c71'''
URL_GOOGLE = '''http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}'''
# URL_TDT = '''http://yingxiang2019.geo-compass.com/api/wmts?layer=s%3Azjw&style=time%3D1576222648262&tilematrixset=w&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image%2Fjpeg&TileMatrix={z}&TileCol={x}&TileRow={y}&threshold=100'''

TOKEN_EXPIRATION = 30 * 24 * 3600

# ip address
IPADDR = UTILS.get_host_ip()

# extent
MIN_T_EXTENT = 0.0042
MIN_P_EXTENT = 0.0014
MAX_P_EXTENT = 0.0098

# minimum building area
MIN_BUILDING_AREA = 50

# if open debug mode
# DEBUG_MODE = True
DEBUG_MODE = False
