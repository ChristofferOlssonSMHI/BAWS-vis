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
    # data_path = r'C:\Temp\baws_reanalys\clipped_archive\corrected_geoms'
    # data_path = r'C:\Temp\baws_reanalys\2022\corrected_geoms'
    data_path = r'C:\Temp\baws_reanalys\aggragated_archive'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location,
    # we set the export path here.
    s.setting.set_export_directory(
        path=r'C:\Temp\baws_reanalys\aggragated_archive')

    # If we want to save data to a specific location,
    # we set the export path here.
    # s.setting.set_export_directory(path=None)

    generator = generate_filepaths(s.data_path, pattern='aggregation_',
                                   endswith='.tiff')

    # Loop through the file-generator and aggregate the data.
    # aggregation is a numpy 2d-array
    aggregation = aggregation_annuals(generator)

    # Export the aggragation in a tiff file.
    # WARNING! tiff files only handles integer data with values <=100.
    # The benefit of tiff-files are the super compressed format
    s.export_data(
        data=aggregation,
        writer='text',
        file_name='aggregation_2002-2022.txt'
    )
