# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-28 11:00

@author: a002028

"""
import numpy as np
import rasterio as rio


def raster_writer(name, array, raster_meta):
    with rio.open(name, 'w+', **raster_meta) as out:
        out.write(array.astype(np.uint8), 1)
    out.close()