# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-28 10:15

@author: a002028

"""
import os
import time
import numpy as np
import pandas as pd
from bawsvis.config import Settings
from bawsvis.session import Session
from bawsvis.readers.raster import raster_reader
from bawsvis.readers.text import np_txt_reader
from bawsvis.readers.shape import shape_reader
from bawsvis.readers.dictionary import pandas_reader
from bawsvis.plotting.map import PlotMap
from bawsvis.writers.raster import raster_writer
from bawsvis.utils import generate_filepaths, Grid, transform_ref_system
from bawsvis.interpolate import get_interpolated_df

import shapely
from shapely.geometry import Polygon
import fiona
from fiona.crs import to_string
import rasterio as rio
from rasterio.features import shapes
import geopandas as gp
import descartes


def area2transform_baws1000_sweref99tm():
    crs = rio.crs.CRS.from_string('+init=epsg:3006')
    west, south, east, north = (-49739.0, 5954123.0, 1350261.0, 7354123.0)
    height, width = (1400, 1400)
    transform = rio.transform.from_bounds(west, south,
                                          east, north,
                                          width, height)
    return crs, transform, (height, width)


def shapeify(rst_path, export_path=None):
    rst = rio.open(rst_path)
    array = rst.read()
    array = array[0]
    array = array.astype(int)

    print('shapeify:', rst_path)
    shape_list = get_shapes_from_raster(array)

    fname = rst_path.replace('.tiff', '.shp')

    if export_path:
        fname = os.path.join(export_path, os.path.basename(fname))

    schema = {'properties': [('class', 'int')], 'geometry': 'Polygon'}

    crs, transform, area_shape = area2transform_baws1000_sweref99tm()

    with fiona.open(fname, 'w', driver='ESRI Shapefile', crs=to_string(crs), schema=schema) as dst:
        dst.writerecords(shape_list)


def get_shapes_from_raster(raster):
    shapes_with_properties = []

    crs, transform, area_shape = area2transform_baws1000_sweref99tm()

    classes = {int(cls): {'class': int(cls)} for cls in np.unique(raster)}
    classes[0] = None

    mask = None

    for i, (s, v) in enumerate(shapes(raster, mask=mask, transform=transform)):
        if v == 0:
            continue
        shapes_with_properties.append({'properties': classes[int(v)], 'geometry': s})

    return shapes_with_properties


def get_geodataframe(shape_list):
    print('get_geodataframe..')
    gf_dict = {'geometry': [], 'class': []}

    for s in shape_list:

        if type(s['geometry']['coordinates'][0]) == list:
            poly = Polygon(s['geometry']['coordinates'][0])
        else:
            poly = Polygon(s['geometry']['coordinates'])

        if not poly.is_empty:
            if poly.area:
                gf_dict['class'].append(s['properties']['class'])
                gf_dict['geometry'].append(poly)

    return gp.GeoDataFrame(gf_dict)


def get_daily_stats(generator):
    stat_dict = {}
    million = 10 ** 6
    for shp_path in generator:
        file_name = os.path.basename(shp_path)
        date_str = ''.join(filter(str.isdigit, file_name))
        print('get_daily_stats', file_name)
        gf = gp.read_file(shp_path)
        boolean_bloom = gf['class'].isin([2, 3])

        if any(boolean_bloom):
            boolean_subsurface_bloom = gf['class'] == 2
            boolean_surface_bloom = gf['class'] == 3

            bloom_area = gf.loc[boolean_bloom, :].geometry.area.sum() / million
            subsurface_bloom_area = gf.loc[boolean_subsurface_bloom, :].geometry.area.sum() / million
            surface_bloom_area = gf.loc[boolean_surface_bloom, :].geometry.area.sum() / million

            bloom_area = round(bloom_area, 1)
            surface_bloom_area = round(surface_bloom_area, 1)
            subsurface_bloom_area = round(subsurface_bloom_area, 1)
        else:
            bloom_area = 0
            surface_bloom_area = 0
            subsurface_bloom_area = 0

        stat_dict[date_str] = {'daily_bloom_area': bloom_area,
                               'surface_area': surface_bloom_area,
                               'subsurface_area': subsurface_bloom_area}
    return stat_dict


def get_weekly_stats(generator):
    stat_dict = {}
    million = 10 ** 6
    for shp_path in generator:
        file_name = os.path.basename(shp_path)
        date_str = ''.join(filter(str.isdigit, file_name))
        print('get_weekly_stats', file_name)
        gf = gp.read_file(shp_path)
        boolean_bloom = gf['class'] > 0

        if any(boolean_bloom):
            bloom_area = gf.loc[boolean_bloom, :].geometry.area.sum() / million
            bloom_area = round(bloom_area, 1)
        else:
            bloom_area = 0

        stat_dict[date_str] = {'weekly_bloom_area': bloom_area}

    return stat_dict


def aggregation_annuals(file_generator, mask=None, reader='raster'):
    """

    :param reader:
    :param file_generator:
    :param mask:
    :param only_surface:
    :return:
    """
    arrays = []
    for fid in file_generator:
        print(fid)
        if reader == 'raster':
            array = raster_reader(fid)
        else:
            array = np_txt_reader(fid)

        # Exclude areas marked with class value 2 or 3 outside of our "valid_baws_area".
        # Mask value 1 marks valid area; Masked value 0 marks not valid area
        if mask:
            array = np.where(mask == 0, 0, array)

        arrays.append(array)

    # Two loops? in case we want to lift out the part below..
    agg_array = arrays[0]
    if len(arrays) == 1:
        pass
    else:
        for scene in arrays[1:]:
            agg_array = agg_array + scene

    return agg_array


def raster_aggregation(file_generator, mask=None, only_surface=False, reader='raster'):
    """

    :param reader:
    :param file_generator:
    :param mask:
    :param only_surface:
    :return:
    """
    arrays = []
    zeros = np.array(())
    for fid in file_generator:
        print(fid)
        if reader == 'raster':
            array = raster_reader(fid)
        else:
            array = np_txt_reader(fid)

        if not zeros.shape[0]:
            zeros = np.zeros(array.shape)

        # Exclude areas marked with class value 2 or 3 outside of our "valid_baws_area".
        # Mask value 1 marks valid area; Maske value 0 marks not valid area
        if mask:
            array = np.where(mask == 0, 0, array)

        if only_surface:
            array = np.where(array == 3, 1, zeros)
        else:
            array = np.where(np.logical_or(array == 2, array == 3), 1, zeros)

        arrays.append(array)

    # Two loops? in case we want to lift out the part below..
    agg_array = arrays[0]
    if len(arrays) == 1:
        pass
    else:
        for scene in arrays[1:]:
            agg_array = agg_array + scene

    return agg_array


def get_interpolated_data_table(data):
    """
    Hardcoded to fit BAWS statistics.
    :param data:
    :return:
    """
    df = pd.DataFrame({'timestamp': data.columns,
                       'daily_bloom_area': data.loc['daily_bloom_area', :],
                       'surface_area': data.loc['surface_area', :],
                       'subsurface_area': data.loc['subsurface_area', :],
                       'weekly_bloom_area': data.loc['weekly_bloom_area', :],
                       })
    new_df = pd.DataFrame()
    for parameter in ['daily_bloom_area', 'surface_area', 'subsurface_area', 'weekly_bloom_area']:
        param_df = get_interpolated_df(df, 'timestamp', parameter)
        param_df = param_df.transpose()
        if new_df.empty:
            new_df = pd.DataFrame(columns=param_df.loc['x', :].values, index=[parameter])
            new_df.loc[parameter] = param_df.loc['y'].values
        else:
            new_df.loc[parameter] = param_df.loc['y'].values

    return new_df.astype(float)


def get_interpolated_statistics_table(data):
    """
    Hardcoded to fit BAWS statistics.
    :param data:
    :return:
    """
    df = pd.DataFrame({'timestamp': data.columns,
                       'daily_mean': data.loc['daily_mean', :],
                       'daily_std_u': data.loc['daily_std_u', :],
                       'daily_std_l': data.loc['daily_std_l', :],
                       'weekly_mean': data.loc['weekly_mean', :],
                       'weekly_std_u': data.loc['weekly_std_u', :],
                       'weekly_std_l': data.loc['weekly_std_l', :],
                       })
    new_df = pd.DataFrame()
    for parameter in ['daily_mean', 'daily_std_u', 'daily_std_l', 'weekly_mean', 'weekly_std_u', 'weekly_std_l']:
        param_df = get_interpolated_df(df, 'timestamp', parameter)
        param_df = param_df.transpose()
        if new_df.empty:
            new_df = pd.DataFrame(columns=param_df.loc['x', :].values, index=[parameter])
            new_df.loc[parameter] = param_df.loc['y'].values
        else:
            new_df.loc[parameter] = param_df.loc['y'].values

    return new_df.astype(float)


def get_statistics(file_path):
    """"""
    data = pandas_reader(file_path)
    data.rename(columns={c: pd.Timestamp(str(c)) for c in data.columns}, inplace=True)
    # df = get_interpolated_data_table(data)

    data = data.transpose()
    summer_dates = pd.date_range('20200601', '20200831')
    stats = {'summer_dates': summer_dates,
             'daily_mean': [], 'daily_std_u': [], 'daily_std_l': [],
             'weekly_mean': [], 'weekly_std_u': [], 'weekly_std_l': []}

    for date in summer_dates:
        boolean = (data.index.month == date.month) & (data.index.day == date.day)
        daily = data.loc[boolean, 'daily_bloom_area']
        weekly = data.loc[boolean, 'weekly_bloom_area']

        daily_mean = round(daily.mean(), 1)
        daily_std = round(daily.std(), 1)
        weekly_mean = round(weekly.mean(), 1)
        weekly_std = round(weekly.std(), 1)

        stats['daily_mean'].append(daily_mean)
        stats['daily_std_u'].append(round(daily_mean + daily_std, 1))
        daily_std_l = round(daily_mean - daily_std, 1)
        if daily_std_l < 0:
            daily_std_l = 0
        stats['daily_std_l'].append(daily_std_l)

        stats['weekly_mean'].append(weekly_mean)
        stats['weekly_std_u'].append(round(weekly_mean + weekly_std, 1))
        weekly_std_l = round(weekly_mean - weekly_std, 1)
        if weekly_std_l < 0:
            weekly_std_l = 0
        stats['weekly_std_l'].append(weekly_std_l)

    return stats


if __name__ == "__main__":
    # settings = Settings()

    data_path = '...\\Manuell_algtolkning'

    s = Session(data_path=data_path)

    generator = generate_filepaths(s.data_path,
                                   pattern='cyano_daymap_',
                                   endswith='.shp',
                                   only_from_dir=True)

    # df = get_statistics_from_shapefiles(generator)


    # print('get_shapes_from_raster')
    # shape_list = get_shapes_from_raster(data)
    # gdf = get_geodataframe(shape_list)
    #
    # patches = get_matplotlib_patches(gdf, map_obj=plot.map)
    # plot.plot_patches(patches)
