# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-09-01 12:11

@author: a002028

"""
import json
import pandas as pd


def json_reader(file_path):
    with open(file_path, 'r') as fd:
        data = json.load(fd)
    return data


def pandas_reader(file_path):
    return pd.read_json(file_path)
