import shapefile
import geojson
import shapely
from shapely import geometry
import pyproj
import functools
import json
import fiona


def project(shape, source, target):
    """Projects a geometry from one coordinate system into another.

    Args:
      shape: the geometry to project.
      source: the source EPSG spatial reference system identifier.
      target: the target EPSG spatial reference system identifier.

    Returns:
      The projected geometry in the target coordinate system.
    """

    project = functools.partial(pyproj.transform, pyproj.Proj(
        init=source), pyproj.Proj(init=target))

    return shapely.ops.transform(project, shape)


# feature to shape,projection,shape to feature.yul
def geojson_project(collection, source, target):
    # with open(geojson_path) as fp:
        # collection = geojson.load(fp)

    shapes = [shapely.geometry.shape(feature["geometry"])
              for feature in collection["features"]]
    features = []
    for shape in shapes:
        if not shape.is_simple or not shape.is_valid:
            continue
        projected = project(shape, source, target)
        feature = geojson.Feature(geometry=shapely.geometry.mapping(
            projected))
        features.append(feature)
    collection_projected = geojson.FeatureCollection(features)
    return collection_projected


def shp2geojson(shp_path):
    # read the shapefile
    reader = shapefile.Reader(shp_path)
    fields = reader.fields[1:]
    field_names = [field[0] for field in fields]
    buffer = []
    # shapeRecords = reader.shapeRecords()
    for sr in reader.shapeRecords():
        atr = dict(zip(field_names, sr.record))
        try:
            geom = sr.shape.__geo_interface__
            buffer.append(dict(type="Feature",
                               geometry=geom, properties=atr))
        except:
            print('要素不可用。要素信息：%s' % str(sr.record))
    jsonstr = json.dumps({"type": "FeatureCollection",
                          "features": buffer}, indent=2)
    return json.loads(jsonstr)


def geojson2shp(collection, shp_path):
    shapes = [geometry.shape(feature["geometry"])
              for feature in collection["features"]]
    schema = {
        'geometry': 'Polygon',
        'properties': {},
    }

    # Write a new Shapefile
    with fiona.open(shp_path, 'w', 'ESRI Shapefile', schema) as c:
        for shape in shapes:
            # delete area smaller than 0.00**1
            if shape.area < 0.00000001:
                continue
            c.write({
                'geometry': shapely.geometry.mapping(shape),
                'properties': {},
            })
    # Write a prj file
    prj_str = '''GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]]'''
    prj_path = shp_path.replace('.shp', '.prj')
    with open(prj_path, 'w') as f:
        f.write(prj_str)
        f.close()

        # if __name__ == "__main__":
        # DATA_PATH = SETTING.ROBOSAT_DATASET_PATH + "./dataset/predict_1583054722.123778"
        # DATA_PATH = "."
        # shp_path = DATA_PATH + "/regularized_footprints.shp"
        # shp4326_path = DATA_PATH + "/building4326.shp"
        # regularized_json_path = DATA_PATH+"/regularized.json"
        # json4326 = DATA_PATH+"/regular_4326.json"
        # shp_to_geojson(shp_path,regularized_json_path)
        # projected_json = geojson_project(
        #     regularized_json_path, "epsg:3857", "epsg:4326")
        # with open(json4326, 'r') as rg:
        #     geojson4326 = json.load(rg)
        #     geojson2shp(geojson4326, shp4326_path)
