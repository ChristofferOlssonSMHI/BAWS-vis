# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 13:11

@author: a002028

"""
# from qgis.core import QgsVectorLayer
import geopandas as gp


# class QGISShapeReaderBase(object):
#     """
#     """
#     def __init__(self):
#         super(QGISShapeReaderBase, self).__init__()
#
#     @staticmethod
#     def read(*args, **kwargs):
#         """
#         :param args:
#         :param kwargs:
#         :return:
#         """
#         layer = QgsVectorLayer(*args)
#         if not layer.isValid():
#             print("Layer failed to load!")
#         else:
#             return layer


class GeoPandasReaderBase(object):
    """
    """
    def __init__(self):
        super(GeoPandasReaderBase, self).__init__()

    @staticmethod
    def read(*args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        print(args)
        return gp.read_file(*args, **kwargs)


class NoneReaderBase(object):
    """
    Dummy base
    """
    def __init__(self):
        super(NoneReaderBase, self).__init__()

    @staticmethod
    def read(*args, **kwargs):
        print('Warning! No shape was read due to unrecognizable datatype')


def shape_reader(reader_type, *args, **kwargs):
    """
    :param reader_type:
    :param args:
    :param kwargs:
    :return:
    """
    if reader_type is 'geopandas':
        base = GeoPandasReaderBase
    # elif reader_type is 'qgis':
    #     base = QGISShapeReaderBase
    else:
        base = NoneReaderBase


    class ShapeReader(base):
        """
        """
        def __init__(self):
            super(ShapeReader, self).__init__()

    sr = ShapeReader()
    return sr.read(*args, **kwargs)
