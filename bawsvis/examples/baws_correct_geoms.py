#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-01 11:15

@author: johannes
"""
import sys
sys.path.append(r'C:\Utveckling\BAWS-vis')
sys.path.append(r'C:\Utveckling\BAWS-vis\bawsvis')
import numpy as np
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import correct_shapefile, ExteriorLog
import pandas as pd
from pathlib import Path
import time
import warnings
warnings.filterwarnings('ignore')


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive'
    # data_path = r'C:\Temp\baws_reanalys\aggragated_archive'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    data_path = r'C:\Temp\baws_reanalys\tiff_archive'
    # data_path = r'C:\Temp\baws_reanalys\tiff_archive\corrected'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=data_path)
    s.setting.set_export_directory(path=r'C:\Temp\baws_reanalys\tiff_archive\corrected')
    # s.setting.set_export_directory(path=r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms')
    # s.setting.set_export_directory(path=r'C:\Temp\baws_reanalys\aggragated_archive\corrected_geoms')

    # Init log. Purpose: save info about multipolygon exterior geometries.
    ExteriorLog()

    # Generate filepaths
    generator = generate_filepaths(s.data_path, pattern='cyano_daymap_', endswith='.shp')
    # generator = generate_filepaths(s.data_path, pattern='cyano_daymap_2021', endswith='.shp')
    # generator = generate_filepaths(s.data_path, pattern='cyano_weekmap', endswith='.shp')

    not_working = []
    time_values = []
    print('looping..')
    for fid in generator:
        name = Path(fid).stem
        # print(name)
        start_time = time.time()
        try:
            correct_shapefile(fid, export_path=s.setting.export_directory)
            time_value = round(time.time() - start_time, 1)
            time_values.append(time_value)

            print(f'{name} - Timeit: {time_value} s -- Average: '
                  f'{np.array(time_values).mean().round(0)} s')
        except:
            print('NOT WORKING', name)
            not_working.append(name)
