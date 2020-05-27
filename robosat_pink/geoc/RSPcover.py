import os
import sys
import shutil
import multiprocessing

from robosat_pink.tools import cover
from robosat_pink.geoc import config as CONFIG, params, utils

multiprocessing.set_start_method('spawn', True)


def main(dsPath,geojson,out):
    params_cover = params.Cover(
        dir=dsPath,
        bbox=None, 
        geojson=geojson,
        cover=None,
        raster=None,
        sql=None,
        pg=None,
        no_xyz=None,
        zoom=18,
        extent=None,
        splits=None,
        out=out)
    cover.main(params_cover)
    
    return True
# 2 mins
