# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 09:48

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import raster_aggregation_ice
from datetime import datetime
import os


if __name__ == "__main__":
    # Set path to data directory
    data_path = r'C:\Temp\ice_data'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)

    # Generate filepaths
    generator = generate_filepaths(s.data_path,
                                   pattern='seaice_',
                                   endswith='.tiff',
                                   only_from_dir=True)
    min_date = datetime.strptime('20190731', '%Y%m%d')
    max_date = datetime.strptime('20200701', '%Y%m%d')
    file_list = []
    for f in generator:
        time = os.path.basename(f).split('_')[1].split('.')[0]
        date = datetime.strptime(time, '%Y%m%d%H%M%S')
        if (date > min_date) and (date < max_date):
            file_list.append(f)
            # print(f)
    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    aggregation = raster_aggregation_ice(file_list)
    #
    # # Export the aggragation in a tiff file.
    # # WARNING! tiff files only handles integer data with values <=100.
    # # The benefit of tiff-files are the super compressed format
    s.export_data(data=aggregation,
                  file_name='aggregation_{}_{}.tiff'.format(min_date.year, max_date.year),
                  writer='raster')
