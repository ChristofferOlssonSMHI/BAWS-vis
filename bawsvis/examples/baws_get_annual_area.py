# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-06-17 22:02
@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import get_shapes_from_raster, get_geodataframe
import rasterio as rio
import numpy as np


if __name__ == "__main__":
    # Set path to data directory
    rst_path = r'C:\Temp\baws_reanalys\aggragated_archive\aggregation_2022.tiff'
    # rst_path = r'C:\Utveckling\BAWS-vis\bawsvis\export\aggregation_only_surface_2014.tiff'
    # rst_path = r'C:\Utveckling\BAWS-vis\bawsvis\export\aggregation_2020.tiff'

    rst = rio.open(rst_path)
    array = rst.read()
    array = np.where(array[0].astype(int) > 0, 1, 0)
    shape_list = get_shapes_from_raster(array)
    gf = get_geodataframe(shape_list)
    print(gf.area.sum() / 1000000)

    # Create the Session object
    # s = Session(data_path=data_path)
    #
    # generator = generate_filepaths(s.data_path,
    #                                pattern='cyano_daymap_',
    #                                endswith='.tiff',
    #                                only_from_dir=True)

