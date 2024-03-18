# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-28 10:31

@author: a002028

"""
import os
from bawsvis.config import Settings
from bawsvis.writers.raster import raster_writer
from bawsvis.writers.dictionary import json_writer
from bawsvis.writers.text import np_text_writer


class Session:
    """Doc."""

    def __init__(self, data_path=None):
        self.setting = Settings()
        self.data_path = data_path

    def export_data(self, data=None, file_name=None, writer='raster'):
        """Doc."""
        file_name = os.path.join(self.setting.export_directory, file_name)
        print('file_name', file_name)
        if writer == 'raster':
            raster_writer(file_name, data, self.setting.raster_template_meta)
        elif writer == 'json':
            json_writer(file_name, data)
        elif writer == 'text':
            np_text_writer(data, file_name)