# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-01 11:49

@author: a002028

"""
import json


def json_writer(file_path, data, indent=4):
    with open(file_path, "w") as outfile:
        json.dump(data, outfile, indent=indent)

