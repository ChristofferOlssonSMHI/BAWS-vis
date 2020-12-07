# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 09:48

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.data_handler import raster_aggregation


# if __name__ == "__main__":
#     # Set path to data directory
#     data_path = '...\\Manuell_algtolkning'
#
#     # Create the Session object
#     s = Session(data_path=data_path)
#
#     # If we want to save data to a specific location, we set the export path here.
#     # s.setting.set_export_directory(path=None)
#
#     # Generate filepaths
#     generator = generate_filepaths(s.data_path,
#                                    pattern='cyano_daymap_',
#                                    endswith='.tiff',
#                                    only_from_dir=True)
#
#     # Loop through the file-generator and aggregate the data.
#     # aggregation is a numpy 2d-array
#     aggregation = raster_aggregation(generator)
#
#     # Export the aggragation in a tiff file.
#     # WARNING! tiff files only handles integer data with values <=100.
#     # The benefit of tiff-files are the super compressed format
#     s.export_data(data=aggregation,
#                   file_name='aggregation_2020.tiff',
#                   writer='raster')

if __name__ == "__main__":
    # Set path to data directory
    data_path = 'C:\\Temp\\baws_reanalys\\tiff_archive'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)
    for year in range(2002, 2010):
        year = str(year)

        # Generate filepaths
        generator = generate_filepaths(s.data_path,
                                       pattern='cyano_daymap_' + year,
                                       endswith='.tiff',
                                       only_from_dir=True)

        # Loop through the file-generator and aggregate the data.
        # aggregation is a numpy 2d-array
        aggregation = raster_aggregation(generator)

        # Export the aggragation in a tiff file.
        # WARNING! tiff files only handles integer data with values <=100.
        # The benefit of tiff-files are the super compressed format
        s.export_data(data=aggregation,
                      file_name='aggregation_%s.tiff' % year,
                      writer='raster')
