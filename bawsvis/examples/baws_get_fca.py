#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-17 10:43

@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.writers.dictionary import json_writer
from bawsvis.readers.dictionary import json_reader
from bawsvis.data_handler import get_area
import geopandas as gp
import os


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms\clipped_archive'

    # Create the Session object
    s = Session(data_path=data_path)

    files = generate_filepaths(data_path, pattern='cyano_daymap_2022',
                               endswith='.shp')
    stat = json_reader(os.path.join(
        s.setting.export_directory, 'stats_all_v2022_2.json'))

    for fid in files:
        print(fid)
        gf = gp.read_file(fid)
        date = fid.split('_')[-1].replace('.shp', '')

        # If the cloud polygons are clipped to the valid cyano area.
        # boolean_cloud = gf['class'] == 1
        # if boolean_cloud.any():
        #     valid_area = 359429. - (gf[boolean_cloud].area.sum() / 1000000.)
        # else:
        #     valid_area = 359429.

        valid_area = 359429. - stat[date]['cloud_area']

        boolean_bloom = gf['class'].isin((2, 3))
        if boolean_bloom.any():
            fca = (gf[boolean_bloom].area.sum() / 1000000.) / valid_area
        else:
            fca = 0.

        stat[date]['fca'] = fca

    out_file_path = os.path.join(
        s.setting.export_directory, 'stats_all_v2022_3.json')
    json_writer(out_file_path, stat)
