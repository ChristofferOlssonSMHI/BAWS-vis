# Copyright (c) 2020 SMHI, Swedish Meteorological and Hydrological Institute 
# License: MIT License (see LICENSE.txt or http://opensource.org/licenses/mit).
"""
Created on 2020-08-31 11:27

@author: a002028

"""
from bawsvis.session import Session
from bawsvis.plotting import PlotMap
import matplotlib.pyplot as plt
import os
import pickle
import rasterio as rio
import numpy as np
import pandas as pd


def read_raster(path):
    rst = rio.open(path)
    array = rst.read()
    return array[0]


if __name__ == "__main__":

    s = Session()
    file = r'C:\Temp\Satellit\olci_output\composite\7_day_comp_{TIMESTAMP}.tiff'

    for date in pd.date_range(start='2017-02-01', end='2017-05-31'):
        date_string = date.strftime('%Y%m%d')
        print(date_string)

        data = read_raster(file.format_map({'TIMESTAMP': date_string}))
        if np.isnan(data).all():
            continue

        with open('west_sea_map.pickle', 'rb') as openfile:
            plot = pickle.load(openfile)

        plot.set_label_text(f'7 day composite - {date_string}')

        plot._draw_mesh(p_color=True, data_mat=data)
        plot._save_figure(
            os.path.join(
                s.setting.export_directory,
                f'7day_composite_{date_string}.png'
            )
        )
        plt.close(plot.map_figure)

    # file = r'C:\Temp\Satellit\olci_output\composite\7_day_comp_20170530.tiff'
    # data = read_raster(file)
    # latitude_array = np.load(r'C:\Utveckling\TESTING\satpy_test\latitude_baws300.npy')
    # longitude_array = np.load(r'C:\Utveckling\TESTING\satpy_test\longitude_baws300.npy')
    #
    # start_time = time.time()
    #
    # map_frame = {'lat_min': 54.5, 'lat_max': 60.,
    #              'lon_min': 8.2, 'lon_max': 15.5}
    # plot = PlotMap(
    #     cbar_label='Chl (µg/l)',
    #     cmap_step=2,
    #     max_tick=10,
    #     min_tick=0,
    #     map_frame=map_frame,
    #     resolution='h',
    #     text='7 day composite - 20170312'
    # )
    #
    # plot._draw_map(lat_mat=latitude_array,
    #                lon_mat=longitude_array)
    #
    # with open('west_sea_map.pickle', 'wb') as file:
    #     pickle.dump(plot, file)

    # with open('west_sea_map.pickle', 'rb') as openfile:
    #     plot = pickle.load(openfile)
    #
    # plot._draw_mesh(p_color=True, data_mat=data)
    # plot._save_figure(
    #     os.path.join(
    #         s.setting.export_directory,
    #         '7day_composite_20170312.png'
    #     )
    # )
    # print("Timeit:--%.5f sec" % (time.time() - start_time))
