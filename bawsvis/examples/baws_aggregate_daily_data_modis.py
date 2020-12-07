# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 09:48

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import raster_aggregation


if __name__ == "__main__":
    # Set path to data directory
    data_path = 'E:\\Johannes_exjobb\\MODIS_data\\outdata\\attribute_data\\BAWS'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)
    for year in range(2019, 2021):
        year = str(year)

        # Generate filepaths
        generator = generate_filepaths(s.data_path,
                                       pattern='BAWS_' + year,
                                       endswith='.txt',
                                       only_from_dir=False)

        # Loop through the file-generator and aggregate the data.
        # aggregation is a numpy 2d-array
        aggregation = raster_aggregation(generator, reader='text')

        # Export the aggragation
        s.export_data(data=aggregation,
                      file_name='aggregation_%s.txt' % year,
                      writer='text')
