# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-28 11:23

@author: a002028

"""
import os
import sys
from bawsvis import utils
from bawsvis.readers.raster import raster_reader
from bawsvis.readers.text import np_txt_reader


class Settings:
    """Doc."""

    def __init__(self, coordinates_settings='baws1000_sweref99tm'):
        self.base_directory = os.path.dirname(os.path.realpath(__file__))
        self.export_directory = '\\'.join([self.base_directory, 'export', ''])
        etc_path = '\\'.join([self.base_directory, 'etc', ''])
        self._load_settings(etc_path)
        self._load_standard_coordinates(etc_path, coordinates_settings)

    def __setattr__(self, name, value):
        """
        Defines the setattr for object self
        :param name: str
        :param value: any kind
        :return:
        """
        if name == 'dir_path':
            pass
        elif isinstance(value, str) and 'path' in name:
            name = ''.join([self.base_directory, value])
        elif isinstance(value, dict) and 'paths' in name:
            self._check_for_paths(value)
        super().__setattr__(name, value)

    def _check_for_paths(self, dictionary):
        """
        Since default path settings are set to sirena base folder
        we need to add that base folder to all paths
        :param dictionary: Dictionary with paths as values and keys as items..
        :return: Updates dictionary with local path (self.dir_path)
        """
        for item, value in dictionary.items():
            if isinstance(value, dict):
                self._check_for_paths(value)
            elif 'path' in item:
                dictionary[item] = ''.join([self.base_directory, value])

    def _load_settings(self, etc_path):
        """
        :param etc_path: str, local path to settings
        :return: Updates attributes of self
        """
        print('Loading tiff settings..')
        paths = utils.generate_filepaths(etc_path, pattern='.tiff')
        settings = {}
        for p in paths:
            file_name = os.path.basename(p).replace('.tiff', '')
            settings[file_name], settings[file_name + '_meta'] = raster_reader(p, include_meta=True)

        self.set_attributes(self, **settings)

    def _load_standard_coordinates(self, etc_path, coord_setting):
        """
        """
        print('Loading coordinates settings..')
        paths = utils.generate_filepaths(etc_path, pattern=coord_setting, endswith='.txt')
        settings = {}
        for p in paths:
            file_name = os.path.basename(p).replace('.txt', '')
            file_name = file_name.replace(coord_setting, 'array')
            settings[file_name] = np_txt_reader(p)

        self.set_attributes(self, **settings)

    def set_export_directory(self, path=None):
        """
        :param path:
        :return:
        """
        if path:
            if os.path.isdir(path):
                self.export_directory = path
            else:
                raise(FileNotFoundError,
                      'Could not find the given path: %s\nUsing standard export path (%s) instead'
                      % (path, self.export_directory))
        else:
            raise (FileNotFoundError,
                   'No path given. Using standard export path (%s) instead' % self.export_directory)

    @staticmethod
    def set_attributes(obj, **kwargs):
        """
        #TODO Move to utils?
        With the possibility to add attributes to an object which is not 'self'
        :param obj: object
        :param kwargs: Dictionary
        :return: sets attributes to object
        """
        for key, value in kwargs.items():
            setattr(obj, key, value)


if __name__ == "__main__":
    settings = Settings()
    print(settings.latitude_array)
