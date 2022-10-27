# -*- coding: utf-8 -*-
"""
Created on 2020-09-18 10:26

@author: a002028
"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import aggregation_annuals
import rasterio as rio
import os
import matplotlib.pyplot as plt


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\baws_reanalys\aggragated_archive'

    # Create the Session object
    s = Session(data_path=data_path)

    # Generate filepaths
    generator = generate_filepaths(s.data_path, pattern='aggregation_', endswith='.tiff')

    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    rst = rio.open('test_mask2.tiff')
    mask = rst.read()
    mask = mask[0].astype(int)
    aggregation = aggregation_annuals(generator, mask=mask)

    # Export the aggragation in a tiff file.
    # WARNING! tiff files only handles integer data with values <=100.
    # The benefit of tiff-files are the super compressed format
    # s.export_data(data=aggregation, file_name='2002-2021_aggregation.txt',
    #               writer='text')
