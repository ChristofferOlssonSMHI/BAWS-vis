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
    data_path = r'C:\Temp\baws_reanalys\tiff_archive\corrected'
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    s.setting.set_export_directory(
        # path=r'C:\Temp\baws_reanalys\2022\corrected_geoms\clipped_archive'
        path=data_path
    )

    # Generate filepaths
    generator = generate_filepaths(
        s.data_path,
        pattern='cyano_weekmap_',
        endswith='.tiff'
    )

    # Loop through the file-generator and shapeify raster data.
    for rst_path in generator:
        print(rst_path)
        # shapeify(rst_path, export_path=s.setting.export_directory)
        shapeify_weekly(rst_path, export_path=s.setting.export_directory)
