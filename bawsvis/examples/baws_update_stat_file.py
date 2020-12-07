# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-01 15:50

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.readers.dictionary import json_reader
from bawsvis.writers.dictionary import json_writer
from bawsvis.utils import recursive_dict_update


if __name__ == "__main__":
    file_path_1 = 'C:/Utveckling/BAWS-vis/bawsvis/export/stats_2020.json'
    file_path_2 = 'C:/Utveckling/baws_reanalys/stat_dict_daily_stats_all.json'

    data = json_reader(file_path_1)
    data_2 = json_reader(file_path_2)

    data_2 = recursive_dict_update(data_2, data)

    out_file_path = file_path_1.replace('stats_2020', 'stats_all')
    json_writer(out_file_path, data_2)
