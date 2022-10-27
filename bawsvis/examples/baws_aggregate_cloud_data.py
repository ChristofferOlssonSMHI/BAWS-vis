#!/usr/bin/env python3
"""
Created on 2021-10-11 15:30

@author: johannes
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import raster_cloud_aggregation


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_tempo\data_2021'

    # Create the Session object
    s = Session(data_path=data_path)

    # Generate filepaths
    generator = generate_filepaths(s.data_path,
                                   pattern='cyano_daymap_202108',
                                   endswith='.tiff',
                                   only_from_dir=True)

    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    aggregation = raster_cloud_aggregation(generator)

    # Export the aggragation in a tiff file.
    # WARNING! tiff files only handles integer data with values <=100.
    # The benefit of tiff-files are the super compressed format
    s.export_data(data=aggregation,
                  file_name='cloud_aggregation_2021_august.tiff',
                  writer='raster')
