# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-01 08:45

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import shapeify, shapeify_weekly


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_tempo\baws_ws_2021\test_interkalibrering\cyano_daymap_20210601.tiff'

    # Create the Session object
    s = Session(data_path=data_path)

    # Loop through the file-generator and shapeify raster data.
    # shapeify(data_path, export_path=s.setting.export_directory)
    # shapeify_weekly(data_path, export_path=s.setting.export_directory)

    print(s.setting.export_directory)
