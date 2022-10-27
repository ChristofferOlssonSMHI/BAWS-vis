# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 09:48

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import aggregation_annuals


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Utveckling\BAWS-vis\bawsvis\export'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)

    # Generate filepaths
    generator = generate_filepaths(s.data_path,
                                   pattern='Cumu_',
                                   endswith='.txt',
                                   only_from_dir=True)

    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    aggregation = aggregation_annuals(generator, reader='text')

    # Export the aggragation
    s.export_data(data=aggregation,
                  file_name='modis_aggregation_2002-2020.txt',
                  writer='text')
