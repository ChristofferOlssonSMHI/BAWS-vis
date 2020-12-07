# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 13:08

@author: a002028

"""
import numpy as np
import pandas as pd


def np_text_writer(array, path):
    np.savetxt(path, array, delimiter='\t', fmt='%1.0f')


def text_writer(path, dataframe, index=False, encoding='cp1252'):
    # dataframe = pd.DataFrame()
    dataframe.to_csv(
        path,
        index=index,
        encoding=encoding,
    )
