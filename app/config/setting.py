TOKEN_EXPIRATION = 30 * 24 * 3600

# building outline PostGIS data table using by training label
BUILDINGS_TABLE = "BUIA"

# tianditu and google map remote sensing wmts url
URL_TDT = '''https://t1.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=4830425f5d789b48b967b1062deb8c71'''
URL_GOOGLE = '''http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}'''
# URL_TDT = '''http://yingxiang2019.geo-compass.com/api/wmts?layer=s%3Azjw&style=time%3D1576222648262&tilematrixset=w&Service=WMTS&Request=GetTile&Version=1.0.0&Format=image%2Fjpeg&TileMatrix={z}&TileCol={x}&TileRow={y}&threshold=100'''

# config.toml and checkpoint.pth files path
ROBOSAT_DATA_PATH = "data"

# dataset to training or predicting
ROBOSAT_DATASET_PATH = "dataset"
