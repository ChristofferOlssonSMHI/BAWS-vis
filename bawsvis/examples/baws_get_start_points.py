#!/usr/bin/env python
# Copyright (c) 2022 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2022-06-27 09:36

@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.writers.dictionary import json_writer
from bawsvis.readers.dictionary import json_reader
from bawsvis.data_handler import get_area
import geopandas as gp
from shapely.ops import unary_union
import os


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'

    # Create the Session object
    s = Session(data_path=data_path)

    data = {}
    for year in range(2002, 2023):
        # Generate filepaths
        generator = generate_filepaths(
            s.data_path, pattern=f'cyano_daymap_{year}', endswith='.shp'
        )

        # Loop through the file-generator extract statistics..
        for day_path in generator:
            gf = gp.read_file(day_path)
            boolean = gf['class'].isin([2, 3])
            if boolean.any():
                print(day_path)
                boundary = gp.GeoSeries(
                    unary_union(gf.loc[boolean, 'geometry'])
                )
                point = boundary.centroid
                data.setdefault('year', []).append(year)
                data.setdefault('centroid', []).append(point)
                break
