# -*- coding: utf-8 -*-
"""
Created on 2020-09-18 09:22

@author: a002028

"""
from bawsvis.utils import generate_filepaths
from bawsvis.session import Session
from bawsvis.readers.text import np_txt_reader
import numpy as np
import os


if __name__ == "__main__":
    # Set path to data directory
    data_path = '...N_FIX\\Result\\Cumu_annual_data'

    # Create the Session object
    s = Session(data_path=data_path)

    generator = generate_filepaths(s.data_path,
                                   pattern='Cumu_',
                                   endswith='.txt',
                                   only_from_dir=True)

    # If we want to save data to a specific location, we set the export path here.
    # s.setting.set_export_directory(path=None)
    for fid in generator:
        print(os.path.basename(fid))
        array = np_txt_reader(fid)

        array = np.where(array < 0, 0, array)

        s.export_data(data=array,
                      file_name=os.path.basename(fid),
                      writer='text')
