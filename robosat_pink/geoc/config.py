# PostgreSQL Connection String
# POSTGRESQL = "host='localhost' dbname='tdt2018' user='postgres' password='postgres'"
POSTGRESQL = "host='172.16.100.140' dbname='tdt2018' user='postgres' password='postgres'"

# building outline PostGIS data table using by training label
BUILDING_TABLE = "BUIA"

# remote sensing image tiles download host url
WMTS_HOST = "http://127.0.0.1:5000/v1/wmts"

# tianditu and google map remote sensing wmts url
URL_TDT = '''https://t1.tianditu.gov.cn/DataServer?T=img_w&x={x}&y={y}&l={z}&tk=8971e4c7b3640d506c2dc111221af6a0'''
URL_GOOGLE = '''http://ditu.google.cn/maps/vt/lyrs=s&x={x}&y={y}&z={z}'''

# wmts_xyz_proxy port
FLASK_PORT = 5000
