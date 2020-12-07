# -*- coding: utf-8 -*-
"""
Created on 2020-09-18 10:26

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import aggregation_annuals


if __name__ == "__main__":
    # Set path to data directory
    data_path = 'C:\\Utveckling\\BAWS-vis\\bawsvis\\export'

    # Create the Session object
    s = Session(data_path=data_path)

    # Generate filepaths
    generator = generate_filepaths(s.data_path,
                                   pattern='Cumu_',
                                   endswith='.txt',
                                   only_from_dir=True)

    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    aggregation = aggregation_annuals(generator, reader='text')

    # Export the aggragation in a tiff file.
    # WARNING! tiff files only handles integer data with values <=100.
    # The benefit of tiff-files are the super compressed format
    s.export_data(data=aggregation,
                  file_name='period_aggregation.txt',
                  writer='text')
