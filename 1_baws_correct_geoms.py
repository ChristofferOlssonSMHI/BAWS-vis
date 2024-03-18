#!/usr/bin/env python3
# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute.
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2021-11-01 11:15

@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import correct_shapefile
from bawsvis.data_handler import ExteriorLog


if __name__ == "__main__":
    # Set path to data directory
    # data_path = r'C:\Temp\baws_tempo\data_2021'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive'
    # data_path = r'C:\Temp\baws_reanalys\aggragated_archive'
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    data_path = r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=data_path)
    s.setting.set_export_directory(path=r'C:\Arbetsmapp\BAWS\Årsrapport 2023\Data_test\corrected_geoms')
    # s.setting.set_export_directory(path=r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms')
    # s.setting.set_export_directory(path=r'C:\Temp\baws_reanalys\aggragated_archive\corrected_geoms')

    # Init log. Purpose: save info about multipolygon exterior geometries.
    ExteriorLog()

    # Generate filepaths
    generator = generate_filepaths(s.data_path, pattern='cyano_daymap_', endswith='.shp')
    # generator = generate_filepaths(s.data_path, pattern='cyano_daymap_2021', endswith='.shp')
    # generator = generate_filepaths(s.data_path, pattern='cyano_weekmap', endswith='.shp')

    for fid in generator:
        print(fid)
        correct_shapefile(fid, export_path=s.setting.export_directory)
