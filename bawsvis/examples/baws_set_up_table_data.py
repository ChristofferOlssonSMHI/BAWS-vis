# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 13:07

@author: a002028

"""
from bawsvis.utils import generate_filepaths, recursive_dict_update
from bawsvis.session import Session
from bawsvis.data_handler import get_daily_stats, get_weekly_stats


if __name__ == "__main__":
    # Set path to data directory
    data_path = '...\\Manuell_algtolkning'

    # Create the Session object
    s = Session(data_path=data_path)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)

    # Generate filepaths (daily)
    generator = generate_filepaths(s.setting.export_directory,
                                   pattern='cyano_daymap_',
                                   endswith='.shp',
                                   only_from_dir=True)

    # Loop through the file-generator and aggregate the data.
    stats_daily = get_daily_stats(generator)

    # Generate filepaths (weekly)
    generator = generate_filepaths(s.data_path,
                                   pattern='cyano_weekmap_',
                                   endswith='.shp',
                                   only_from_dir=True)

    # Loop through the file-generator and aggregate the data.
    stats_weekly = get_weekly_stats(generator)

    stats = recursive_dict_update(stats_daily, stats_weekly)

    # # Export the table in json file.
    s.export_data(data=stats,
                  file_name='stats_2020.json',
                  writer='json')
